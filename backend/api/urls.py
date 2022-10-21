from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipesViewSet,
                    SetPasswordAndSubscribeViewSet, TagsViewSet,
                    FavoriteViewSet, ShoppingCartViewSet)

app_name = 'api'

router = DefaultRouter()

router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'users', SetPasswordAndSubscribeViewSet, basename='users')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(
    r'recipes/(?P<recipe_id>[\d]+)/favorite',
    FavoriteViewSet,
    basename='favorite'
)
router.register(
    r'recipes/(?P<recipe_id>[\d]+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shoping_cart'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
