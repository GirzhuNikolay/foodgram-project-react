import django_filters as filters

from recipes.models import Ingredient


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='take')

    class Meta:
        model = Ingredient
        fields = ('name',)
