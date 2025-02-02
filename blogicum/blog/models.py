from django.db import models
from django.utils.timezone import now

from core.constants import CHAR_LENGTH, USER
from core.models import BaseModel, FullBaseModel


class PublishedPostManager(models.Manager):
    """Класс для получения опубликованных постов."""

    def get_queryset(self):
        return super().get_queryset().filter(
            pub_date__lte=now(),
            is_published=True,
            category__is_published=True,
        )


class Post(FullBaseModel):
    """Класс для описания таблицы Post в БД."""

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        help_text=(
            'Если установить дату в будущем — '
            'можно делать отложенные публикации.'
        ),
        default=now
    )
    author = models.ForeignKey(
        USER, on_delete=models.CASCADE, verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    comment_count = models.IntegerField(default=0)

    image = models.ImageField(
        'Изображение',
        upload_to='post_images',
        blank=True
    )

    objects = models.Manager()
    published_objects = PublishedPostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return self.title


class Category(FullBaseModel):
    """Класс для описания таблицы Category в БД."""

    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseModel):
    """Класс для описания таблицы Location в БД."""

    name = models.CharField(
        max_length=CHAR_LENGTH, verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Класс для описания таблицы Comment в БД."""

    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(USER, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
