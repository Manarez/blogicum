from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404

from blog.models import Category, Post, Comment
from blog.forms import CommentForm


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class CategoryPublishedMixin:

    def dispatch(self, request, *args, **kwargs):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)

        if not category.is_published:
            raise Http404('Категория снята с публикации.')

        return super().dispatch(request, *args, **kwargs)


class ModelPostMixin:
    model = Post


class ModelAndFormCommentMixin:
    model = Comment
    form_class = CommentForm


class GetSuccessUrlPostMixin:

    def get_success_url(self):
        post = self.get_object()
        return reverse_lazy('blog:post_detail', args=(post.id,))


class GetSuccessUrlProfileMixin:

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('blog:profile', args=(username,))
