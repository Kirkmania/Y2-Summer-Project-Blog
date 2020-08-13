from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Comment, Category, CV
from .forms import PostForm, CommentForm, CVForm
from .decorators import unauthenticated_user, allowed_users

# Create your views here.
# NOTE: My first view creation :o
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

# Must make sure the extra arg has the EXACT same name as in urls.py. Is this django-only? Or python?
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# New post form page
@login_required
@allowed_users(allowed_roles=['admin'])
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # Usually commit is true, but in this case we want to add author THEN save!
            post.author = request.user
            # post.published_date = timezone.now()          # removed to separate drafting and publishing
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# Alternative postnew view! NOTE: NOT IN USE
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    #fields = '__all__'
    #fields = ('title', 'text')

# Edit existing post page
@login_required
@allowed_users(allowed_roles=['admin'])
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()          # removed to separate drafting and publishing 
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# Show unpublished posts
@login_required
@allowed_users(allowed_roles=['admin'])
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

# Publish draft post
@login_required
@allowed_users(allowed_roles=['admin'])
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

# Delete existing post
@login_required
@allowed_users(allowed_roles=['admin'])
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()                           # Model.delete is standard django method.
    return redirect('post_list')

# Add comment to post           TODO: If user is logged in, change form such that name field not required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
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
class AddCategoryView(CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = '__all__'

def category_view(request, category):
    category_posts = Post.objects.filter(category__iexact=category.replace('-', ' '))
    return render(request, 'blog/categories.html', {'category': category.title().replace('-', ' '), 'category_posts':category_posts})

def cv(request):
    form = CVForm()
    return render(request, 'blog/cv.html', {'form': form})