# from django.urls import path
# from .views import register_view,about, edit_profile,profile_view
# from django.contrib.auth.views import LoginView, LogoutView
# from django.views.generic import TemplateView
# from django.contrib.auth import views as auth_views

from django.urls import path
from .views import register_view, about, edit_profile, profile_view
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    # path("login/", CustomLoginView.as_view(), name="login"),
    # path("register/", register_view, name="register"),
    # path("logout/", LogoutView.as_view(next_page="home"), name="logout"),

    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("contact/", TemplateView.as_view(template_name="contact.html"), name="contact"),
    path('profile/', profile_view,name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='users/change_password.html'), name='change_password'),

]
