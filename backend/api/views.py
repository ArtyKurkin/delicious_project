from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, Recipe,
                            ShoppingCart, Subscribe, Tag)
from users.models import User

from .utils import get_shopping_list
from .filters import IngredientFilter, RecipeFilter
from .mixins import RetrieveListViewSet
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (CustomUserSerializer, FavoriteSerializer,
                          IngredientSerializer, PasswordSerializer,
                          RecipeCreateSerializer, RecipeListSerializer,
                          SubscribeSerializer, TagSerializer,
                          ShoppingCartSerializer)


class SetPasswordAndSubscribeViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(methods=['POST'],
            detail=False,
            permission_classes=(IsAuthenticated,))
    def set_password(self, request, pk=None):
        user = self.request.user
        serializer = PasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'],
            detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,))
    def subscribe(self, request, *args, **kwargs):
        user = request.user
        user_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=user_id)
        if user == author:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscribe = Subscribe.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if subscribe.exists():
                data = {
                    'errors': 'Вы уже подписаны на автора!'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            Subscribe.objects.create(user=user, author=author)
            serializer = SubscribeSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not subscribe.exists():
                data = {
                    'errors': 'Вы не подписаны на автора!'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagsViewSet(RetrieveListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientsViewSet(RetrieveListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def get_queryset(self):
        serializer = self.get_serializer()
        queryset = Recipe.objects.all()
        return serializer.get_serializer_class(queryset)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        user = request.user
        main_list = get_shopping_list(user)
        response = HttpResponse(main_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="Cart.txt"'
        return response


class FavoriteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)

    @action(detail=True, methods=['DELETE'])
    def delete(self, request, *args, **kwargs):
        favorite = Favorite.objects.filter(
            user=request.user,
            recipe__id=kwargs.get('recipe_id')
        )
        if not favorite.exists():
            return Response(
                data='Запись не существует.',
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)

    @action(detail=True, methods=['DELETE'])
    def delete(self, request, *args, **kwargs):
        shoping_cart = ShoppingCart.objects.filter(
            user=request.user,
            recipe__id=kwargs.get('recipe_id')
        )
        if not shoping_cart.exists():
            return Response(
                data='Запись не существует.',
                status=status.HTTP_400_BAD_REQUEST
            )
        shoping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
