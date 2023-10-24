from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, IngredientViewSet, RecipeViewset,
                    SubscribeView, SubscriptionsList, TagViewSet,
                    AuthToken)


router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewset, basename='recipes')

urlpatterns = [
    path('auth/token/login/',
         AuthToken.as_view(),
         name='login'),
    path('users/subscriptions/', SubscriptionsList.as_view({'get': 'list'})),
    path('users/<int:user_id>/subscribe/', SubscribeView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
