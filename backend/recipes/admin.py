from django.contrib import admin

from .models import (FavoriteRecipe, Follow, Ingredient, Recipe,
                     RecipeIngredient, ShoppingCart, Tag)

L_P_P = 10


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    min_num = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('id', 'name', 'author', 'pub_date', 'get_favorite_count',)
    list_filter = ('author__username', 'name', 'tags',)
    search_fields = ('author__username', 'name', 'tags__name',)
    filter_horizontal = ('tags',)
    empty_value_display = '-пусто-'

    def get_favorite_count(self, obj):
        return obj.favorite.count()

    get_favorite_count.short_description = 'Добавлений в избранное'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = L_P_P
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_follow',)
    list_filter = ('author',)
    search_fields = ('author__username', 'user__username',)

    def get_follow(self, obj):
        return (f'Пользователь {str(obj.user).capitalize()} '
                f'подписан на {str(obj.author).capitalize()}.')

    get_follow.short_description = 'Подписки на пользователей'


@admin.register(FavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_favorite',)
    search_fields = ('recipe__name', 'user__username',)

    def get_favorite(self, obj):
        return f'"{obj.recipe}" добавлен пользователем {obj.user}.'

    get_favorite.short_description = 'Избранные рецепты'


@admin.register(ShoppingCart)
class ShoppingAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_shopping',)
    list_filter = ('recipe',)
    search_fields = ('recipe__name',)

    def get_shopping(self, obj):
        return (f'"{obj.recipe}" добавлен в покупки '
                f'пользователем {str(obj.user).capitalize()}.')

    get_shopping.short_description = 'Рецепты добавленные в покупки.'
