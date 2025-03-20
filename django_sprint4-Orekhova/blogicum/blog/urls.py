"""
Маршруты приложения blog.

Этот файл содержит маршруты URL для приложения blog,
включая маршруты для постов, профиля пользователя и категорий.
"""

from django.urls import path

from . import views

app_name = 'blog'

post_url_patterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail',
    ),
    path(
        'posts/<int:pk>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post',
    ),
    path(
        'posts/<post_id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post',
    ),
    path(
        'posts/<post_id>/comment/',
        views.AddCommentView.as_view(),
        name='add_comment',
    ),
    path(
        'posts/<post_id>/edit_comment/<comment_id>/',
        views.EditCommentView.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<post_id>/delete_comment/<comment_id>/',
        views.DeleteCommentView.as_view(),
        name='delete_comment',
    ),
]

profile_url_patterns = [
    path(
        'profile/<str:username>/',
        views.ProfileView.as_view(),
        name='profile',
    ),
    path(
        'edit/',
        views.EditProfileView.as_view(),
        name='edit_profile',
    ),
]

category_url_patterns = [
    path(
        '<slug:category_slug>/',
        views.CategoryPostsView.as_view(),
        name='category_posts',
    ),
]

urlpatterns = (
    post_url_patterns + profile_url_patterns + category_url_patterns
)
