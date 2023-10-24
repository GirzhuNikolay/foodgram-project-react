from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    '''Модель пользователя'''

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        db_index=True,
    )

    username = models.CharField(
        verbose_name='Логин',
        max_length=150,
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Введены недопустимый символ'
        )]
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    password = models.CharField(
        max_length=254,
        verbose_name='Пароль'
    )
    is_admin = models.BooleanField(
        verbose_name='Администратор',
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'username', 'first_name', 'last_name'

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:50]
