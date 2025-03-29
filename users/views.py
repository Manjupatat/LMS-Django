# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import RegisterForm,UserCreationForm,ProfileUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


# class CustomLoginView(LoginView):
#     template_name = 'users/login.html'

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('home')

def about(request):
    return render(request, 'about.html')


# @login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

