"""
Модели для приложения blog.

Содержит модели для категорий, местоположений, публикаций и комментариев.
"""

from core.models import BaseModel
from django.db import models
from django.contrib.auth import get_user_model

# Получение модели пользователя
User = get_user_model()


class Category(BaseModel):
    """
    Модель для категорий постов.

    Категории используются для группировки публикаций
    по тематическим разделам.
    """

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta:
        """
        Meta-класс для модели Category.
        """
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.title)


class Location(BaseModel):
    """
    Модель для местоположений.

    Местоположения используются для указания географической привязки
    публикаций.
    """

    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
    )

    class Meta:
        """
        Meta-класс для модели Location.
        """
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return str(self.name)


class Post(BaseModel):
    """
    Модель для публикаций.

    Публикации представляют собой записи, создаваемые пользователями.
    Каждая публикация имеет заголовок, текст, автора, категорию,
    местоположение, изображение и дату публикации.
    """

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField(
        upload_to='blogs_images',
        null=True,
        blank=True,
        verbose_name='Фото',
    )

    class Meta:
        """
        Meta-класс для модели Post.
        """
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    """
    Модель для комментариев к публикациям.

    Комментарии позволяют пользователям оставлять отзывы к публикациям.
    Содержат автора, текст и дату создания.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Автор комментария',
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Публикация',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        """
        Meta-класс для модели Comment.
        """
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return str(self.text)
