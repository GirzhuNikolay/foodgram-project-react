from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Tag, Ingredient
from .serializers import TagSerializer, IngredientSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import viewsets
from .filters import IngredientFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
