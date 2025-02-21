from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404

from blog.models import Category, Post, Comment
from blog.forms import CommentForm


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин для проверки на авторство."""

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class CategoryPublishedMixin:
    """Миксин для проверки, что категория доступна для публикации."""

    def dispatch(self, request, *args, **kwargs):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)

        if not category.is_published:
            raise Http404('Категория снята с публикации.')

        return super().dispatch(request, *args, **kwargs)


class ModelPostMixin:
    """Миксин модели Post."""

    model = Post


class ModelAndFormCommentMixin:
    """Миксин модели и формы Comment."""

    model = Comment
    form_class = CommentForm


class GetSuccessUrlPostMixin:
    """Миксин получения страницы поста для перенаправления."""

    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('blog:post_detail', args=(post.id,))


class GetSuccessUrlProfileMixin:
    """Миксин получения страницы пользователя после перенаправления."""

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('blog:profile', args=(username,))
