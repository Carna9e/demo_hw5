from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User
from .utils import Page


def index(request):
    """Функция главной страницы"""
    post_list = Post.objects.all()
    page_obj = Page(request, post_list, settings.LIMIT)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """функция группы постов"""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = Page(request, post_list, settings.LIMIT)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html/', context)


def profile(request, username):
    """функция страницы порфиля автора"""
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author)
    page_obj = Page(request, post_list, settings.LIMIT)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """функция подробной информации о посте"""
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """функция создания нового поста"""
    # if request.method == 'POST':
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user)
    return render(request, 'posts/create.html', {'form': form})
    # form = PostForm()
    # return render(request, 'posts/create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """функция редактирования поста"""
    post = get_object_or_404(Post, id=post_id)
    if request.user.id != post.author.id:
        return redirect('posts:post_detail', post_id=post.id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.id)
    context = {
        'form': form,
        'is_edit': True,
        'post_id': post_id,
    }
    return render(request, 'posts/create.html', context)
