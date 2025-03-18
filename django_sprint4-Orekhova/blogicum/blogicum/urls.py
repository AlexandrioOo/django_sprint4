"""
URL-конфигурация для проекта blogicum.

Этот модуль содержит маршруты для работы с приложениями проекта,
включая маршруты для администратора, аутентификации,
и статичных страниц.
"""

from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.edit import CreateView
from django.urls import include, path, reverse_lazy

# Настройка обработчиков ошибок
handler403 = 'pages.views.csrf_failure'  # Обработчик ошибки 403
handler404 = 'pages.views.page_not_found'  # Обработчик ошибки 404
handler500 = 'pages.views.internal_server_error'  # Обработчик ошибки 500

# Основные маршруты проекта
urlpatterns = [
    # Главная страница блога
    path('', include('blog.urls')),

    # Маршруты для статичных страниц
    path('pages/', include('pages.urls')),

    # Административный интерфейс
    path('admin/', admin.site.urls),

    # Аутентификация пользователей
    path('auth/', include('django.contrib.auth.urls')),

    # Регистрация нового пользователя
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,  # Путь к медиафайлам
)
