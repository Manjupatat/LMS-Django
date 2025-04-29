from django.urls import path
from .views import home,courses, about, contact_page

urlpatterns = [
    path('', home, name='home'),
    path('courses/',courses,name='courses'),
    path('contact/', contact_page, name='contact'),
    # path('about/', about, name='about'),
]
