from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from .models import LDAPUser, UserProfile


@receiver(post_save, sender=LDAPUser)
def add_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        

@receiver(user_logged_in)
def update_user_profile(sender, request, user, **kwargs):
    user.profile.save()
