from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.urls import reverse
from django.http import Http404

from .forms import CommentForm, PostForm, UserProfileForm
from .models import Post, Category, Comment

PAGINATE_BY = 10  # Константа для пагинации


class PostListView(ListView):
    model = Post
    paginate_by = PAGINATE_BY
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_visible=True  # Исправлено
        ).select_related(
            'author'
        ).prefetch_related(
            'category', 'location'
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            args=[self.object.author.username]
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None  # Инициализация атрибута

    def test_func(self):
        self.object = self.get_object()
        return (
            self.request.user.is_authenticated
            and self.object.author == self.request.user
        )

    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return redirect(
                reverse(
                    'blog:post_detail',
                    kwargs={'post_id': self.kwargs['pk']}
                )
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return super().get_queryset().filter(
            author=self.request.user
        )

    def get_success_url(self):
        return reverse('blog:index')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self, queryset=None):
        # Разрешаем доступ к посту, если пользователь - автор
        post = get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        )
        if post.is_published or post.author == self.request.user:
            return post
        raise Http404("Пост недоступен")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.get_object().comments.all().order_by(
            'created_at'
        )
        return context


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        profile = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return Post.objects.filter(
            author=profile
        ).select_related(
            'author'
        ).prefetch_related(
            'comments', 'category', 'location'
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return context


class CategoryPostsView(ListView):
    model = Post
    paginate_by = PAGINATE_BY
    template_name = 'blog/category.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = None  # Инициализация атрибута

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category=self.category
        ).select_related(
            'author', 'category', 'location'
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.username}
        )

    def get_object(self, queryset=None):
        return self.request.user


class BaseCommentView(LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'comments.html'

    def get_post(self):
        return get_object_or_404(
            Post,
            id=self.kwargs.get('post_id')
        )

    def form_valid(self, form):
        form.instance.post = self.get_post()
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddCommentView(BaseCommentView, CreateView):
    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs.get('post_id')}
        )


class EditCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None  # Инициализация атрибута

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            raise PermissionDenied(
                'Вы не авторизованы для редактирования этого комментария.'
            )
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment,
            id=self.kwargs.get('comment_id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('post_id')
        return context

    def get_success_url(self):
        return reverse('blog:index')


class DeleteCommentView(BaseCommentView, DeleteView):
    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs.get('post_id')}
        )
