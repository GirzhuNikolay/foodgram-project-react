
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    '''Фильтр ингредиентов.'''

    search_param = 'name'
