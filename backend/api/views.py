from django.db.models import Exists, OuterRef
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from djoser import views
from rest_framework import exceptions, mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (Ingredient, FavoriteRecipe, Follow,
                            Recipe, RecipeIngredient, ShoppingCart, Tag)
from users.models import User

from .filters import IngredientSearchFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from .serializers import (IngredientSerializer, FollowSerializer,
                          GetTokenSerializer,
                          RecipeCreateSerializer, RecipeListSerializer,
                          ShortRecipeSerializer, TagSerializer)
from .utils import delete, post, forming_pdf


class ListViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)


class AuthToken(ObtainAuthToken):
    """Авторизация"""

    serializer_class = GetTokenSerializer
    permission_classes = (AllowAny,)
    pagination_class = None

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'auth_token': token.key},
                        status=status.HTTP_201_CREATED)


class CustomUserViewSet(views.UserViewSet):

    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=('get', 'patch'),
        serializer_class=FollowSerializer,
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, request):
        user = self.request.user
        user_subscriptions = user.follower.all()
        authors = [item.author.id for item in user_subscriptions]
        queryset = User.objects.filter(pk__in=authors)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('get', 'post', 'delete'),
        serializer_class=(FollowSerializer, ),
        permission_classes=(IsAuthenticated, )
    )
    def get_subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)

        if self.request.method == 'POST':
            if user == author:
                raise exceptions.ValidationError(
                    'Нельзя подписываться на себя'
                )
            if Follow.objects.filter(
                user=user,
                author=author
            ).exists():
                raise exceptions.ValidationError('Подписка уже есть.')

            Follow.objects.create(user=user, author=author)
            serializer = self.get_serializer(author, many=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not Follow.objects.filter(
                user=user,
                author=author
            ).exists():
                raise exceptions.ValidationError(
                    'Подписки нет'
                )

            subscription = get_object_or_404(
                Follow,
                user=user,
                author=author
            )
            subscription.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FollowViewSet(APIView):
    '''Подписка, отмена подписки'''

    permission_classes = (IsAuthenticated,)

    def post(self, request, user_id):
        serializer = FollowSerializer(
            data={'user': request.user.id, 'author': user_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        follow = get_object_or_404(Follow, author=user_id, user=request.user)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowList(ListViewSet):
    '''Списк подписок.'''

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class IngredientViewSet(ListViewSet):
    '''Список ингредиентов'''

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(ListViewSet):
    '''Список тегов.'''

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    '''Рецепты'''

    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly | IsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = Recipe.objects.select_related(
            'author').prefetch_related('tags')
        favorited = self.request.query_params.get('is_favorited')
        shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        author = self.request.query_params.get('author')
        tags = self.request.query_params.getlist('tags')
        if favorited:
            queryset = queryset.filter(favorite__user=self.request.user)
        if shopping_cart:
            queryset = queryset.filter(shopping__user=self.request.user)
        if author:
            queryset = queryset.filter(author=author)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        if self.request.user.is_authenticated:
            return queryset.annotate(
                favorit=Exists(
                    queryset.filter(
                        favorite__user=self.request.user,
                        favorite__recipe=OuterRef('id'),
                    )
                ),
                shoppings=Exists(
                    queryset.filter(
                        shopping__user=self.request.user,
                        shopping__recipe=OuterRef('id'),
                    )
                ),
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return post(
                request, pk, Recipe,
                FavoriteRecipe, ShortRecipeSerializer
            )
        if request.method == 'DELETE':
            return delete(request, pk, Recipe, FavoriteRecipe)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return post(
                request, pk, Recipe,
                ShoppingCart, ShortRecipeSerializer
            )
        if request.method == 'DELETE':
            return delete(request, pk, Recipe, ShoppingCart)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping__user=request.user
        ).values_list(
            'ingredient__name', 'ingredient__measurement_unit', 'amount'
        )
        return FileResponse(
            forming_pdf(ingredients),
            as_attachment=True,
            filename='shopping_cart.pdf',)
