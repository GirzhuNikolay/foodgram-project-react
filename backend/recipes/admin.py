from django.contrib import admin

from recipes.models import (
    Ingredient, Tag, Recipe, IngredientInRecipe,
    Favorite, ShoppingCart,
)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'added_in_favorites')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('added_in_favorites',)
    filter_horizontal = ('tags',)

    def added_in_favorites(self, obj):
        return obj.favorites.all().count()

    added_in_favorites.short_description = 'Количество в избранном'


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount',)
    list_filter = ('ingredient',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('user',)


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(IngredientInRecipe)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
