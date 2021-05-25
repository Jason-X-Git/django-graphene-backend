# code: utf-8 

from os import name
import pytest
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model
from users.models import UserProfile

pytestmark = pytest.mark.django_db


def test_create_user():
    User = get_user_model()
    admin = User.objects.create_superuser(username='admin', password='admin')
    assert admin.is_superuser
    assert admin.username == 'admin'
    assert admin.check_password('admin')
    

def test_user_profile():
    User = get_user_model()
    user = User.objects.create(username='test_user', password='123456')

    # Test if user profile created automatically
    assert isinstance(user, User)
    assert isinstance(user.profile, UserProfile)
    assert user.profile.user is user
    assert user.profile.user.username == 'test_user'


