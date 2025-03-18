"""
Модуль содержит абстрактную модель BaseModel,
которая добавляет общие поля для всех моделей приложения.
"""

from django.db import models


class BaseModel(models.Model):
    """
    Абстрактная модель для добавления общих полей.

    Поля:
    - is_published: Отвечает за публикацию объекта.
    - created_at: Автоматически добавляет время создания объекта.
    """

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        """
        Meta-класс для BaseModel.
        """
        abstract = True
