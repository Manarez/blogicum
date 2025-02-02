from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blog.models import Category, Comment, Post
from core.constants import PAGINATE_BY, USER
from core.mixins import (
    OnlyAuthorMixin, ModelPostMixin,
    ModelAndFormCommentMixin,
    GetSuccessUrlPostMixin, GetSuccessUrlProfileMixin
)
from .forms import CommentForm, PostForm, UserForm


class IndexListView(ModelPostMixin, ListView):
    """View для отображения главной страницы проекта."""

    paginate_by = PAGINATE_BY
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.published_objects.all()


class PostCreateView(
    LoginRequiredMixin, ModelPostMixin, GetSuccessUrlProfileMixin, CreateView
):
    """View для отображения страницы создания поста."""

    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(
    OnlyAuthorMixin, ModelPostMixin, GetSuccessUrlPostMixin, UpdateView
):
    """View для отображения страницы регистрации поста."""

    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        if user.id != post.author_id:
            return HttpResponseRedirect(
                reverse_lazy('blog:post_detail', args=(post.id,))
            )

        return super().dispatch(request, *args, **kwargs)


class PostDetailView(ModelPostMixin, DetailView):
    """View для отображения страницы поста."""

    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        post = self.get_object()
        if user.id != post.author_id and not post.is_published:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comment.select_related('author')
        return context


class PostDeleteView(
    OnlyAuthorMixin, ModelPostMixin, GetSuccessUrlProfileMixin, DeleteView
):
    """View для отображения страницы удаления поста."""

    template_name = 'blog/create.html'


class EditProfileView(GetSuccessUrlProfileMixin, UpdateView):
    """View для отображения страницы редактирования профиля."""

    model = USER
    form_class = UserForm
    template_name = 'blog/user.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDetailListView(ListView):
    """View для отображения страницы профиля."""

    model = USER
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    paginate_by = PAGINATE_BY

    def get_user(self):
        username = self.kwargs.get('username')
        return get_object_or_404(USER, username=username)

    def get_queryset(self):
        if self.request.user == self.get_user():
            return self.get_user().posts.all()
        return self.get_user().posts(manager='published_objects').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user()
        return context


class CategoryListView(ListView):
    """View для отображения страницы с постами из определенной категории."""

    model = Category
    template_name = 'blog/category.html'
    paginate_by = PAGINATE_BY

    def get_category(self):
        return get_object_or_404(
            Category, is_published=True, slug=self.kwargs['category_slug']
        )

    def get_queryset(self):
        return Post.published_objects.filter(
            category=self.get_category()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class CommentCreateView(
    ModelAndFormCommentMixin, UserPassesTestMixin, CreateView
):
    """View для отображения страницы создания комментария."""

    def test_func(self):
        return self.request.user.is_authenticated

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = post
        comment.save()
        post.comment_count = post.comment.count()
        post.save()
        return redirect('blog:post_detail', pk=post.pk)


class CommentEditView(
    ModelAndFormCommentMixin, OnlyAuthorMixin,
    GetSuccessUrlPostMixin, UpdateView
):
    """View для отображения страницы редактирования комментария."""

    template_name = 'blog/comment.html'


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    """View для отображения страницы удаления комментария."""

    model = Comment
    template_name = 'blog/comment.html'

    def get_post(self):
        return self.get_object().post

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=(self.get_post().id,))

    def delete(self, request, *args, **kwargs):
        post = self.get_post()
        response = super().delete(request, *args, **kwargs)
        post.comment_count = post.comment.count()
        post.save()
        return response
