from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('courses/', course_list, name='course_list'),
    path('contact/',contact,name="contact"),
    path('', course_list, name='courses'),
    path('<int:course_id>/', course_detail, name='course_detail'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.course_detail, name='course_detail_lesson'),
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),  # <-- Add this
    path('course/<int:course_id>/discussion/', views.course_discussion, name='course_discussion'),
]
