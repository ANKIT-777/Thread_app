from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User
from app.models import Post
from django.contrib.auth.decorators import login_required
from django.urls import reverse





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



@login_required
def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        userprofile, created = UserProfile.objects.get_or_create(user=user)
        posts = Post.objects.filter(user=user)
        context = {
            'user': user,
            'userprofile': userprofile, 
            'posts': posts
        }
        return render(request, 'user.html', context)
    else:
        return render(request, 'login.html')

 





@login_required
def create_post(request):
    context = {}  

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            posts = Post.objects.all()
            context = {'posts': posts, 'form': form}
            return redirect('home_page')
    else:
        form = PostForm()

    posts = Post.objects.all()
    context['form'] = form  
    context['posts'] = posts 

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
            return redirect('thread', post_id=post.id)
    form = CommentForm()
    
    comments = Comment.objects.filter(post=post)
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'form': form,
        'comments': comments,
        'userprofile' : userprofile
    }
    return render(request, 'thread.html', context)





@login_required
def thread(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    user = post.user
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    context = {
        'post': post,
        'comments': comments,
        'postuser': userprofile
    }
    return render(request, 'thread.html', context)


def home_page(request):
    posts = Post.objects.all()
    user = request.user
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    
    
    context = {
        'posts': posts,
        'userprofile' : userprofile,
        }
    return render(request,'home.html',context)



def user_view(request,user_id):
    user = get_object_or_404(User, id=user_id)
    userprofile, created = UserProfile.objects.get_or_create(user=user)
    
    posts = Post.objects.filter(user=user)
    
    logged_profile = UserProfile.objects.get(user = request.user)
    
    is_following = logged_profile.following.filter(username=user.username).exists()
    print(is_following)
    context = {
        'userprofile' : userprofile,
        'is_following': is_following,
        'posts' : posts
    }
    
    return render(request, 'user_template.html', context)


@login_required
def like_post(request, post_id):
    logged_user = request.user
    post = Post.objects.get(id=post_id)

    if logged_user in post.liked_by.all():

        post.likes_count -= 1
        post.liked_by.remove(logged_user)
    else:

        post.likes_count += 1
        post.liked_by.add(logged_user)

    post.save()
    return redirect(reverse('home_page'))


def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    user_to_follow_profile = UserProfile.objects.get(user=user_to_follow)
    logged_user = request.user  
    
    if user_to_follow_profile.followers.filter(id=logged_user.id).exists():
        logged_user.userprofile.following.remove(user_to_follow)
        user_to_follow_profile.followers.remove(logged_user)
    else:
        user_to_follow_profile.followers.add(logged_user)
        logged_user.userprofile.following.add(user_to_follow)
        
        
        
    context = {
        'userprofile' : user_to_follow_profile
        }
    return redirect('user_view', user_id=user_id)



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect(reverse('home_page'))


def edit_post(request,edit_post):
    if request.method == "POST":
        form = Post(request.POST,request.FILES)
        if form.is_valid():
            thread, created = Post.objects.get_or_create(user=request.user)
            thread.content = thread.cleaned_data['content']
            thread.image = thread.cleaned_data['image']
            thread.video = thread.cleaned_data['video']
            thread.save()
            return redirect(reverse('home_page'))
            
    return redirect('home_page')        
    
    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            userprofile, created = UserProfile.objects.get_or_create(user=request.user)
            userprofile.name = form.cleaned_data['name']
            userprofile.bio = form.cleaned_data['bio']
            userprofile.instagram_url = form.cleaned_data['instagram_url']
            userprofile.profile_image = form.cleaned_data['profile_image']
            userprofile.save()
            
            return redirect(reverse('user_profile'))

    else:
        form = UserProfileForm()

    userinfo = UserProfile.objects.filter(user=request.user)
    context = {'userinfo': userinfo, 'form': form}
    return render(request, 'user.html', context)

    