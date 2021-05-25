# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.conf import settings

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, 
                                choices=((item, item) for item in ('High', 'Middle', 'Low')),
                                default='Low')
    
    def __str__(self) -> str:
        return f'{self.user.username} - {self.message} - {self.creation_date}'
