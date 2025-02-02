from django.contrib import admin

from .models import Comment, Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс для описания админ-зоны модели Category приложения Blog"""

    list_display = (
        'is_published',
        'created_at',
        'title',
        'description',
        'slug'
    )
    list_editable = (
        'is_published',
        'slug'
    )
    list_filter = (
        'title',
        'created_at',
        'is_published',
    )
    search_fields = ('title',)
    list_display_links = ('title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс для описания админ-зоны модели Post приложения Blog"""

    list_display = (
        'author',
        'is_published',
        'created_at',
        'pub_date',
        'location',
        'category',
        'text',
    )
    list_editable = (
        'is_published',
        'category',
    )
    list_filter = (
        'author',
        'created_at',
        'is_published',
        'category',
        'location',
    )
    search_fields = (
        'text',
        'author',
    )
    list_display_links = (
        'author',
        'text',
    )


admin.site.register(Location)
admin.site.register(Comment)
