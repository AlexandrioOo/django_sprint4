"""
Обработчики пользовательских ошибок для приложения pages.

Содержит обработчики для 404, 403 (CSRF) и 500 ошибок.
"""

from django.shortcuts import render


def page_not_found(request, exception):  # noqa: W0613
    """Обработчик для ошибки 404: страница не найдена."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason='', exception=None):  # noqa: W0613
    """Обработчик для ошибки CSRF."""
    return render(
        request,
        'pages/403csrf.html',
        {'reason': reason},
        status=403,
    )


def internal_server_error(request):
    """Обработчик для ошибки 500: внутренняя ошибка сервера."""
    return render(request, 'pages/500.html', status=500)
