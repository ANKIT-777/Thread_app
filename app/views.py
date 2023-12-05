from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User
from app.models import Post
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseBadRequest




def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        
        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request,'*Username exist choose another username')
            return redirect('/register/')
        
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        return redirect('/login/')
    return render(request,'register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_profile')
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
            return redirect('/login/')

    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect(reverse('login'))



def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        context = {
            'user': user,
        }
        return render(request, 'user.html', context)
    else:
        return render(request,'login.html')

 
@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
    else:
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'user.html', {'profile_form': profile_form})

 
 
def home_page(request):
    queryset = Post.objects.all()
    context = {
        'thread': queryset,
    }
    posts = Post.objects.all()
    context = {'posts': posts}

    return render(request,'home.html',context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    else:
        form = Post()

    posts = Post.objects.all()
        
    context = {'posts': posts,}
    return render(request, 'home.html', context)


def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.likes_count += 1
    post.save()
    return redirect('home_page')


@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  
            comment.post = post
            comment.save()
            return redirect('home_page')
    form = CommentForm()
    
    comments = Comment.objects.filter(post=post)
    
    context = {
        'form': form,
        'comments': comments,
    }
    
    return render(request, 'home.html', context)




def thread(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)

    context = {
        'post': post,
        'comments': comments,
    }
    
    return render(request, 'thread.html', context)
