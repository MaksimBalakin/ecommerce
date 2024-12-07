
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, CustomUserCreationForm, UserProfileForm
from shop.forms import GoodForm
from shop.models import Good

from django.shortcuts import render, redirect


# def home(request):
#     return render(request, 'users/home.html')

def home(request):
    goods = Good.objects.all()  # Fetch all goods from the database
    return render(request, 'users/home.html', {'goods': goods})



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # redirect to home or dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user  # Get the logged-in user
    form = UserProfileForm(instance=user)  # Create a form instance with user data
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  # Save the updated user info
            return redirect('home')  # Change this to redirect to the home page after saving
    
    return render(request, 'users/profile.html', {'form': form})  # Render the profile template


