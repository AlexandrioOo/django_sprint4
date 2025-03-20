"""
Модели для приложения blog.

Содержит модели для категорий, местоположений, публикаций и комментариев.
"""

from core.models import BaseModel

from django.db import models
from django.contrib.auth import get_user_model

# Получение модели пользователя
User = get_user_model()

# Константы
MAX_TITLE_LENGTH = 256
TEXT_PREVIEW_LENGTH = 50
IMAGE_UPLOAD_PATH = 'blogs_images'


class Category(BaseModel):
    """Модель для категорий постов.

    Категории используются для группировки публикаций
    по тематическим разделам.
    """

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
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
    is_visible = models.BooleanField(
        default=True,
        verbose_name='Видимость',
        help_text='Определяет, будет ли категория отображаться.',
    )

    class Meta:
        """Meta-класс для модели Category."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.title)


class Location(BaseModel):
    """Модель для местоположений.

    Местоположения используются для указания географической привязки
    публикаций.
    """

    name = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        verbose_name='Название места',
    )

    class Meta:
        """Meta-класс для модели Location."""

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return str(self.name)


class Post(BaseModel):
    """Модель для публикаций.

    Публикации представляют собой записи, создаваемые пользователями.
    Каждая публикация имеет заголовок, текст, автора, категорию,
    местоположение, изображение и дату публикации.
    """

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
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
        related_name='posts',
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория',
    )
    image = models.ImageField(
        upload_to=IMAGE_UPLOAD_PATH,
        null=True,
        blank=True,
        verbose_name='Фото',
    )

    class Meta:
        """Meta-класс для модели Post."""

        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    """Модель для комментариев к публикациям.

    Комментарии позволяют пользователям оставлять отзывы к публикациям.
    Содержат автора, текст и дату создания.
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
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
        """Meta-класс для модели Comment."""

        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return str(self.text)[:TEXT_PREVIEW_LENGTH] if self.text else ""
