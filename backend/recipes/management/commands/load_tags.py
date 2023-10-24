from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Создание тэгов'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#00FF00', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#FFFF00', 'slug': 'dinner'},
            {'name': 'Ужин', 'color': '#00FFFF', 'slug': 'supper'}]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Все тэги загружены!'))
