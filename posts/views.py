from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm

def home(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'home.html')

@login_required
def feed(request):
    category = request.GET.get('category', '')
    post_type = request.GET.get('type', '')
    posts = Post.objects.all().select_related('author')
    if category:
        posts = posts.filter(category=category)
    if post_type:
        posts = posts.filter(post_type=post_type)
    posts = posts.filter(
        Q(visibility='open') |
        Q(visibility='branch', target_branch=request.user.branch)
    )
    return render(request, 'posts/feed.html', {
        'posts'    : posts,
        'category' : category,
        'post_type': post_type,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('feed')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post     = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().select_related('author')
    is_liked = post.likes.filter(user=request.user).exists()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment        = form.save(commit=False)
            comment.post   = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'posts/post_detail.html', {
        'post'    : post,
        'comments': comments,
        'form'    : form,
        'is_liked': is_liked,
    })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Post deleted!')
    return redirect('feed')