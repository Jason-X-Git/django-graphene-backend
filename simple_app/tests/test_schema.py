import pytest
from mixer.backend.django import mixer
from simple_app import schema
from graphql_relay.node.node import to_global_id
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

pytestmark = pytest.mark.django_db


def test_message_type():
    instance = schema.MessageType()
    assert instance


def test_resolve_all_messages():
    mixer.cycle(5).blend('simple_app.Message')
    q = schema.Query()
    res = q.resolve_all_messages(None)
    assert res.count() == 5, 'Should return all 5 messages'


def test_resolve_message():
    msg = mixer.blend('simple_app.Message')
    q = schema.Query()
    id = to_global_id('MessageType', msg.pk)
    res = q.resolve_message(info=None, id=id)
    assert res == msg, 'Should return the requested message !'


def test_user_type():
    instance = schema.UserType()
    assert instance


def test_resolve_current_user():
    q = schema.Query()
    req = RequestFactory().get('/')
    req.user = AnonymousUser()
    res = q.resolve_current_user(None,req=req)
    assert res is None, 'Should return None if user is not authenticated'

    user = mixer.blend('users.LDAPUser')
    req.user = user
    res = q.resolve_current_user(None, req=req)
    assert res == user, 'Should return the current user if is authenticated'
