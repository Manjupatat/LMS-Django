from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile
from django.contrib.auth.models import User
class RegisterForm(UserCreationForm):
    is_instructor = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','is_student', 'is_instructor']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo','first_name','last_name','linkedin','github']
   
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

# class ProfileUpdateForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=True)

#     class Meta:
#         model = Profile
#         fields = ['first_name', 'last_name']

#     def __init__(self, *args, **kwargs):
#         super(ProfileUpdateForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].initial = self.instance.user.first_name
#         self.fields['last_name'].initial = self.instance.user.last_name

#     def save(self, commit=True):
#         profile = super().save(commit=False)
#         profile.user.first_name = self.cleaned_data['first_name']
#         profile.user.last_name = self.cleaned_data['last_name']
#         if commit:
#             profile.user.save()
#             profile.save()
#         return profile        