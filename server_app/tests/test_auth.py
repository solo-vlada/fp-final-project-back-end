from warnings import catch_warnings
from ..routes.main import index
from unittest import mock
import pytest, json
import base64

def test_users_get(api):
    resp = api.get('/auth/users')
    assert resp.status == '200 OK'

def test_offers_get(api):
    resp = api.get('/auth/offers')
    assert resp.status == '200 OK'

def test_msg_get(api):
    resp = api.get('/auth/msg/1f4d9382-17ff-11ed-8ac3-704d7b3306bd')
    assert resp.status == '200 OK'

def test_login_post(api):
    resp = api.open('/auth/login', 
        method="post",
        headers={
            'Authorization': 'Basic ' + base64.b64encode(bytes("ben" + ":" + "pass", 'ascii')).decode('ascii')
        })
    assert resp.status == '200 OK'