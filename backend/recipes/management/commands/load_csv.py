import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """Функция загрузки ингредиентов в базу"""
    def import_ingredients(self, file='ingredients.csv'):
        if Ingredient.objects.exists():
            print('Данные для Ingredient уже загружены')
        else:
            with open(f'../data/{file}', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    Ingredient.objects.create(
                        name=row[0],
                        measurement_unit=row[1]
                    )

    def handle(self, *args, **options):
        self.import_ingredients()
        print('Загрузка прошла успешно.')
