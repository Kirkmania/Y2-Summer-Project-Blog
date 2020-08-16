from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Comment, Category, CV
from .forms import PostForm, CommentForm, CVForm
from .decorators import unauthenticated_user, allowed_users

# Create your views here.
# NOTE: My first view creation :o
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    category_menu = Category.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'category_menu': category_menu})

# Must make sure the extra arg has the EXACT same name as in urls.py. Is this django-only? Or python?
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    category_menu = Category.objects.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'category_menu': category_menu})

# New post form page
@login_required
@allowed_users(allowed_roles=['admin', 'author'])
def post_new(request):
    category_menu = Category.objects.all()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # Commit false so can add author before save
            post.author = request.user
            if 'save_and_publish' in request.POST:
                post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'category_menu': category_menu})

# Alternative postnew view! NOTE: NOT IN USE (also should learn about mixins)
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    #fields = '__all__'
    #fields = ('title', 'text')

# Edit existing post page
@login_required
@allowed_users(allowed_roles=['admin', 'author'])
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    category_menu = Category.objects.all()
    if request.user == post.author or request.user.groups.filter(name='admin').exists():
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                if 'save_and_publish' in request.POST:
                    post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form, 'post': post, 'category_menu': category_menu})
    else:
        return redirect('invalid_author', pk=post.pk)

# Show unpublished posts
@login_required
@allowed_users(allowed_roles=['admin', 'author'])
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

# Publish draft post
@login_required
@allowed_users(allowed_roles=['admin', 'author'])
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author or request.user.groups.filter(name='admin').exists():
        post.publish()
        return redirect('post_detail', pk=pk)
    else:
        return redirect('invalid_author', pk=post.pk)

# Delete existing post
@login_required
@allowed_users(allowed_roles=['admin', 'author'])
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author or request.user.groups.filter(name='admin').exists():
        post.delete()                           # Model.delete is standard django method.
        return redirect('post_list')
    else:
        return redirect('invalid_author', pk=post.pk)

def post_invalid_author(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/invalid_author.html', {'post': post})

# Add comment to post           TODO: If user is logged in, change form such that name field not required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.approve()
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
@allowed_users(allowed_roles=['admin'])
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
@allowed_users(allowed_roles=['admin'])
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

# Add category NOTE: TRYING OUT CLASS VIEWS
class AddCategoryView(PermissionRequiredMixin, CreateView): # We have to include mixin arg instead of equivalent decorator.
    permission_required = 'blog.add_category'
    model = Category
    template_name = 'blog/add_category.html'
    fields = '__all__'

def category_view(request, category):
    category_posts = Post.objects.filter(category__iexact=category.replace('-', ' '))
    category_menu = Category.objects.all()
    return render(request, 'blog/categories.html', {'category': category.title().replace('-', ' '), 'category_posts': category_posts, 'category_menu': category_menu})

def cv(request):
    form = CVForm()
    return render(request, 'blog/cv.html', {'form': form})

def handler403(request, exception):
    return render(request, '403.html')