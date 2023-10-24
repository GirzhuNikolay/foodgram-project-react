from rest_framework.filters import SearchFilter


class IngredientSearchFilter(SearchFilter):
    '''Фильтрация ингредиентов.'''

    search_param = 'name'
