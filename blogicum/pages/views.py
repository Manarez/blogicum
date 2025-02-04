from http import HTTPStatus

from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import render

from core.constants import USER


class AboutTemplateView(TemplateView):
    """View для отображения страницы с информацией о проекте."""

    template_name = 'pages/about.html'


class RulesTemplateView(TemplateView):
    """View для отображения страницы с правилами пользования проектом."""

    template_name = 'pages/rules.html'


class UserCreateView(CreateView):
    """View для отображения страницы с формой для создания пользователя."""

    model = USER
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('blog:index')


def page_not_found(request, exception):
    """Функция для переопрееделения шаблона страницы 404"""
    return render(request, 'pages/404.html', status=HTTPStatus.NOT_FOUND)


def csrf_failure(request, reason=''):
    """Функция для переопрееделения шаблона страницы 403"""
    return render(request, 'pages/403csrf.html', status=HTTPStatus.FORBIDDEN)


def server_error(request):
    """Функция для переопрееделения шаблона страницы 500"""
    return render(
        request, 'pages/500.html', status=HTTPStatus.INTERNAL_SERVER_ERROR
    )
