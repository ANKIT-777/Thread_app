from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User




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
    return redirect('/login/')



def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        context = {
            'user': user,
        }
        return render(request, 'user.html', context)
    else:
        return render(request,'login.html')

 
 
 
def home_page(request):
    return render(request,'home.html')


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home_page')  # Replace 'home' with the URL you want to redirect after posting
    else:
        form = PostForm()

    return render(request, 'home.html', {'form': form})
