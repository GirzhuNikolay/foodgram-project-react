from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Tag, Ingredient
from rest_framework.serializers import (
    ModelSerializer, CharField, EmailField, SerializerMethodField)

from users.models import User


class CreateUserSerializer(UserCreateSerializer):
    username = CharField()
    email = EmailField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',)
        extra_kwargs = {'password': {'write_only': True}}


class UsersSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.following.filter(user=user).exists()
        return False


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'unit_of_measurement'
        )
