from django.db import models

from .constants import CHAR_LENGTH


class BaseModel(models.Model):
    """Класс для описания абстрактной модели."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class FullBaseModel(BaseModel):
    """Класс для описания расширенной абстрактной модели."""

    title = models.CharField(max_length=CHAR_LENGTH, verbose_name='Заголовок')

    class Meta:
        abstract = True
