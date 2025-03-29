from django.urls import path
from .views import *

urlpatterns = [
    path('courses/', course_list, name='course_list'),
    path('contact/',contact,name="contact"),
    path('', course_list, name='courses'),
    path('<int:course_id>/', course_detail, name='course_detail'),
]
