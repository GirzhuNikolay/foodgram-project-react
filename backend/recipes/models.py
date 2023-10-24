from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Класс интредиент"""
    name = models.CharField(
        verbose_name='Наименование ингредиента',
        max_length=254,
        help_text='Наименование ингредиента',
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=254,
        help_text='Единица измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[:50].capitalize()


class Tag(models.Model):
    """Класс тег"""

    name = models.CharField(
        max_length=50,
        verbose_name='Hазвание',
        unique=True,
        db_index=True
    )

    color = ColorField(
        default='#17A400',
        max_length=7,
        verbose_name='Цвет',
        unique=True,
        help_text='Цвет в формате HEX кода',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг содержит недопустимый символ'
        )]
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name[:50]


class Recipe(models.Model):
    """Класс рецепт"""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text='Автора рецепта',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        help_text='Название рецепта',
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images',
        help_text='Картинка',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты рецепта',
        through='RecipeIngredient',
        related_name='recipes',
        help_text='Ингредиенты в составе рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег рецепта',
        related_name='recipes',
        help_text='Тег рецепта',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(
                1,
                message='Минимальное время приготовления 1 мин.'
            )
        ],
        help_text='Время приготовления',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        help_text='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:50]


class RecipeIngredient(models.Model):
    """Класс рецепт-интредиент"""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient',
        help_text='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient',
        help_text='Ингредиент',
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                1,
                message='Минимальное количество 1'
            )
        ],
        help_text='Количество',
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='unique_ingredient',
            ),
        ]

    def __str__(self):
        return f'{self.ingredient} в {self.ingredient.measurement_unit}'


class Follow(models.Model):
    """Класс подписки"""

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
        help_text='Подписчик',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='author',
        help_text='Автор',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_follow',
            ),
        ]


class FavoriteRecipe(models.Model):
    """Класс избранное"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite',
        help_text='Пользователь добавивший рецепт',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранное',
        on_delete=models.CASCADE,
        related_name='favorite',
        help_text='Избранный рецепт',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite',
            ),
        ]


class ShoppingCart(models.Model):
    """Класс покупок"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping',
        help_text='Пользователь добавивший покупки',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Покупки',
        on_delete=models.CASCADE,
        related_name='shopping',
        help_text='Рецепт для покупок',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_shoppingcart',
            ),
        ]
