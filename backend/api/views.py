from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Subscribe, Tag)
from users.models import User

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (CustomUserSerializer, FavoriteSerializer,
                          IngredientSerializer, PasswordSerializer,
                          RecipeCreateSerializer, RecipeListSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          TagSerializer)


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
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                {'message': 'пароль изменен!'},
                status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'Неверный данные!'},
            status=status.HTTP_400_BAD_REQUEST
        )

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
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
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


class TagsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
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

    def get_list(self, request, list_model, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        in_list = list_model.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if not in_list:
                list_objects = list_model.objects.create(user=user,
                                                         recipe=recipe)
                if isinstance(list_model, Favorite):
                    serializer = FavoriteSerializer(list_objects.recipe)
                else:
                    serializer = ShoppingCartSerializer(list_objects.recipe)
                return Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not in_list:
                data = {'errors': 'Этого рецепта нет в списке.'}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            in_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['DELETE', 'POST'],
        detail=True,
        permission_classes=(IsAuthenticated, )
    )
    def favorite(self, request, pk=None):
        return self.get_list(request=request, list_model=Favorite, pk=pk)

    @action(
        methods=['DELETE', 'POST'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        return self.get_list(request=request, list_model=ShoppingCart, pk=pk)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__carts__user=request.user.id
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_cart = ['Список покупок:\n--------------']
        for position, ingredient in enumerate(ingredients, start=1):
            shopping_cart.append(
                f'\n{position}. {ingredient["ingredient__name"]}:'
                f' {ingredient["amount"]}'
                f'({ingredient["ingredient__measurement_unit"]})'
            )
        response = HttpResponse(shopping_cart, content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment;filename=shopping_cart.csv'
        )
        return response
