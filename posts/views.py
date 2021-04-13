from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from .settings import POSTS_PER_PAGE


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page': page
    })


@login_required
def follow_index(request):
    follows = get_list_or_404(Follow, user=request.user)
    posts = [post for follow in follows for post in follow.author.posts.all()]
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
        'page': page,
    })


@login_required
def profile_follow(request, username):
    profile = get_object_or_404(User, username=username)
    if not request.user.follower.filter(author=profile).exists():
        request.user.follower.create(author=profile)
    return redirect(request.GET.get('next'))


@login_required
def profile_unfollow(request, username):
    profile = get_object_or_404(User, username=username)
    request.user.follower.filter(author=profile).delete()
    return redirect(request.GET.get('next'))


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {
        'group': group,
        'page': page,
    })


@login_required
def new_post(request):
    form = PostForm(data=request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'post-form.html',
                      {'form': form})
    new_post = form.save(commit=False)
    new_post.author = request.user
    new_post.save()
    return redirect('posts:index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        following = request.user.follower.filter(author=author)
    else:
        following = None
    posts = author.posts.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {
        'author': author,
        'following': following,
        'page': page,
    })


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    if request.user.is_authenticated:
        following = request.user.follower.filter(author=post.author)
    else:
        following = None
    comments = post.comments.all()
    form = PostForm()
    return render(request, 'post.html', {
        'author': post.author,
        'following': following,
        'post': post,
        'form': form,
        'comments': comments,
    })


def add_comment(request, username, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.post = Post.objects.get(pk=post_id)
        new_comment.save()
    return redirect('posts:post', username, post_id)


@login_required
def post_edit(request, username, post_id):
    if request.user.username != username:
        return redirect('posts:post', username=username, post_id=post_id)
    post = get_object_or_404(Post, author=request.user, pk=post_id)
    form = PostForm(
        instance=post,
        data=request.POST or None,
        files=request.FILES or None,
    )
    if not form.is_valid():
        return render(request, 'post-form.html', {
            'form': form,
            'post': post
        })
    form.save()
    return redirect('posts:post', username=username, post_id=post_id)


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
