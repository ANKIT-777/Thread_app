
from django.shortcuts import render,HttpResponse
from .forms import *
from django.contrib.auth import authenticate, login


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user =  authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            return HttpResponse('looged in')
    
        
    return render(request,'login.html')
