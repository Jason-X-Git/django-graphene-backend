from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
import os


class LDAPUser(AbstractUser):
    department = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    office = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}. {self.title}.'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


def upload_picture(instance, file_name):
    return os.path.join(
        'pictures', instance.user.username)


class UserProfile(models.Model):
    user = models.OneToOneField(LDAPUser, related_name='profile',
                                on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=upload_picture,
        blank=True, null=True)
    first_time = models.DateTimeField(auto_now_add=True)
    recent_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.full_name} created @{self.first_time.strftime("%H:%M %Y-%m-%d")}. Recently logged in @{self.recent_time.strftime("%H:%M %Y-%m-%d")}'

