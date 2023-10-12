from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    TagViewSet, IngredientViewSet, UsersViewSet, RecipesViewSet)


app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register('users', UsersViewSet)
router_v1.register('tags', TagViewSet)
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('recipes', RecipesViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
