from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    """Модель пользователя"""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True)
    password = models.CharField(
        "Пароль",
        max_length=150,)
    email = models.EmailField(
        "Электронная почта",
        max_length=254,
        unique=True,)
    first_name = models.CharField(
        "Имя",
        max_length=150,)
    last_name = models.CharField(
        "Фамилия",
        max_length=150,)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]

    def __str__(self):
        return f"{self.username} {self.email}"


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='Подписка на автора уже оформлена'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписываться на себя')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Вы подписались на {self.author}"
