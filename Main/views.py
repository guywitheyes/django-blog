from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import NewPostForm, UserRegisterForm, PostUpdateForm, ConfirmEmailForm
from .models import Post
from .utils import confirm_email_address, send_confirm_email

# Create your views here.
def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Home',
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'Main/home.html', context=context)

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'Main/about.html', context=context)

def author(request, author):
    user = User.objects.filter(username=author).first()
    posts = Post.objects.filter(author=user)
    context = {
        'title': 'Author\'s posts',
        'user': user,
        'posts': posts,
    }
    return render(request, 'Main/author.html', context)

def post_page(request, post_id):
    post = Post.objects.filter(pk=post_id).first()
    if post.author == request.user:
        post_author = True
    else:
        post_author = False

    context = {
        'title': 'Post',
        'post': post,
        'post_author': post_author,
    }
    messages.success(request, post.id)
    return render(request, 'Main/post.html', context)

def new_post(request):
    author = request.user

    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            post = Post()

            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.author = author

            post.save()
            return redirect('home')
    else:
        form = NewPostForm()

    context = {
        'title': 'New Post',
        'form': form,
    }
    return render(request, 'Main/new_post.html', context)

def update(request, post_id):
    post = Post.objects.filter(pk=post_id).first()
    author = post.author

    if request.method == 'POST':
        form = PostUpdateForm(request.POST, initial={'title': post.title, 'content': post.content})
        if form.is_valid():
            form.save(commit=False)

            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.author = author
            post.save()
            
            return redirect('home')

    else:
        form = PostUpdateForm(initial={'title': post.title, 'content': post.content})

    context = {
        'title': 'Update Post',
        'post': post,
        'form': form,
    }
    return render(request, 'Main/update.html', context)
    
def delete(request, post_id):
    post = Post.objects.filter(pk=post_id).first()
    context = {
        'title': 'Delete Post',
        'post': post,
    }
    post.delete()
    return render(request, 'Main/delete.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, message=f'Please confirm your account.')

            username = form.cleaned_data['username']
            email = form.cleaned_data.get('email')
            send_confirm_email(username, email)
            return redirect('confirm')
    else:
        form = UserRegisterForm()

    context = {
        'title': 'Register',
        'form': form
    }
    return render(request, 'Main/register.html', context=context)

def confirm(request):
    if request.method == 'POST':
        form = ConfirmEmailForm(request.POST)
        if form.is_valid():
            code_field = form.cleaned_data['code_field']
            confirm_email_address(code_field)
            
    else:
        form = ConfirmEmailForm()
    context = {
        'title': 'Register',
        'form': form,
    }
    return render(request, 'main/confirm.html', context)

@login_required
def profile(request):
    user = User.objects.filter(username=request.user).first()
    posts = Post.objects.filter(author=user)
    context = {
        'title': 'Profile',
        'posts': posts,
    }
    return render(request, 'Main/profile.html', context=context)
    