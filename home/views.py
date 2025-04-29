# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from courses.models import Course,CustomUser

def home(request):
    # courses = Course.objects.all()
    # return render(request, 'home.html')
    featured_courses = Course.objects.filter(is_featured=True)[:6]
    top_instructors = CustomUser.objects.filter(is_instructor=True)[:4]

    context = {
        'featured_courses': featured_courses,
        'top_instructors': top_instructors,
    }
    return render(request, 'home.html', context)

def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


# def about(request):
#     return render(request, 'about.html')