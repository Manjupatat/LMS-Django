# from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    # pass
    # def __stnr__(self):
    #     retur self.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="profile")
    # profile_photo = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio=models.TextField(blank=True)

    def __str__(self):
        # return f'{self.user.username} Profile'
        return self.user.username 