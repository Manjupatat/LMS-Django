# from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render, redirect
# from django.contrib.auth.views import LoginView
# from .forms import RegisterForm,UserCreationForm,ProfileUpdateForm
# from django.contrib.auth import login, logout
# from django.contrib.auth.decorators import login_required
# from django.models import *

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import RegisterForm,UserCreationForm,ProfileUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from courses.models import *
from django.views import *
# from courses.models import Enrollment



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

# def logout_view(request):
#     logout(request)
#     return redirect('home')
class LogoutView(View):
    def get(self, request):
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
    user=request.user
    user_progress = UserProgress.objects.filter(user=user)
    enrolled_courses = [progress.course for progress in user_progress]

    # enrolled_courses=User
    return render(request, 'users/profile.html',{'enrolled_courses': enrolled_courses,
        'user': user,})


@login_required
def my_courses(request):
    user = request.user
    # enrolled_courses = Course.objects.filter(userprogress__user=user)
    enrolled_courses = Enrollment.objects.filter(user=user).select_related('course')

    return render(request, "users/profile.html", {
        "enrolled_courses": enrolled_courses,
    })
