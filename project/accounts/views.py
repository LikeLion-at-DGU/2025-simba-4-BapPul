from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
def login(request): # {% url 'accounts:login' %}
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(request, username=username, password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('search:home')
    
    else:
      return render(request, 'accounts/login.html')

  elif request.method == 'GET':
    return render(request, 'accounts/login.html')
  
def logout(request): # {% url 'accounts:logout' %}
  auth.logout(request)
  return redirect('search:home')

def start_view(request):
  return render(request, 'accounts/start.html')

def signup(request):
  if request.method == 'POST':
    if request.POST['password'] == request.POST['confirm']:
      user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password']
      )
      nickname = request.POST['nickname']
      school = request.POST['school']

      profile = Profile(user=user, nickname=nickname, school=school)
      profile.save()

      auth.login(request, user)
      return redirect('accounts:login')
    
  return render(request, 'accounts/signup.html')