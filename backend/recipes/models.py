from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Наименование тэга',
        max_length=256,
        unique=True,)
    color = models.CharField(
        'Код Hex',
        max_length=20,
        unique=True,)
    slug = models.SlugField(
        'Слаг Тэга',
        max_length=50,
        unique=True,)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Ингредиент')
    measurement_unit = models.CharField(
        max_length=256,
        verbose_name='Единица измерения')

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'Нименование',
        max_length=200)
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор',)
    text = models.TextField('Описание')
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/',
        blank=True,
        null=True)
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(
            1, message='Время не может быть меньше 1 мин.!')]
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="recipe",)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Ингредиенты в рецепте',
    )
    amount = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1, 'Должен быть хотябы 1 ингредиент')
        ],
        verbose_name='Количество ингредиента'
    )

    class Meta:
        default_related_name = 'ingridients_recipe'
        constraints = [
            UniqueConstraint(
                fields=('ingredient', 'amount'),
                name='unique_ingredient'),
        ]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.ingredient} – {self.amount}'


class Favorite(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="favorite",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="favorite",
    )

    class Meta:
        verbose_name = "Список избранного"
        verbose_name_plural = "Список избранного"
        ordering = ("recipe",)

    def __str__(self):
        return f"{self.user} {self.recipe}"


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="shopping_cart",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="shopping_cart",
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"
        ordering = ("recipe",)

    def __str__(self):
        return f"{self.user} {self.recipe}"
