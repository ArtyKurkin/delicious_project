from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Subscribe, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', )
    search_fields = ('author', 'name', 'tags', )
    list_filter = ('author', 'name', 'tags', )
    inlines = [RecipeIngredientInline, ]
    empty_value_display = '-пусто-'

    def favorites_count(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit', )
    search_fields = ('name', )
    list_filter = ('name', )
    inlines = [RecipeIngredientInline, ]
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug', )
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe', )
    search_fields = ('user', 'recipe', )
    list_filter = ('user', )
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe', )
    search_fields = ('user', 'recipe', )
    list_filter = ('user', )
    empty_value_display = '-пусто-'


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author', )
    search_fields = ('user', )
    list_filter = ('user', )
    empty_value_display = '-пусто-'
