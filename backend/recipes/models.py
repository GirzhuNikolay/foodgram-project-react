from django.contrib.auth import get_user_model
from django.db import models


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
        verbose_name='Количество')
    unit_of_measurement = models.CharField(
        max_length=256,
        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
