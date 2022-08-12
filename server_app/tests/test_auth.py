from ..routes.main import index
from flask import jsonify, json
import base64

def test_users_get(api):
    resp = api.get('/auth/users')
    assert resp.status == '200 OK'

def test_users_get_content(api):
    resp = api.get('/auth/users')
    data = json.loads(resp.get_data(as_text=True))
    assert 'users' in data
    

def test_offers_get(api):
    resp = api.get('/auth/offers')
    assert resp.status == '200 OK'

def test_login_post(api):
    resp = api.open('/auth/login', 
        method="post",
        headers={
            'Authorization': 'Basic ' + base64.b64encode(bytes("ben" + ":" + "pass", 'ascii')).decode('ascii')
        })
    assert resp.status == '200 OK'

def test_msg_get(api):
    login = api.open('/auth/login', 
        method="post",
        headers={
            'Authorization': 'Basic ' + base64.b64encode(bytes("ben" + ":" + "pass", 'ascii')).decode('ascii')
        })

    token = login

    resp = api.get('/auth/msg',
    headers={
            'x-access-tokens': token
        })
    assert resp.status == '200 OK'

def test_msg_get(api): 

    login = api.open('/auth/login', 
        method="post",
        headers={
            'Authorization': 'Basic ' + base64.b64encode(bytes("ben" + ":" + "pass", 'ascii')).decode('ascii')
        })

    token = login

    resp = api.get('/auth/msg',
    headers={
            'x-access-tokens': token
        })
    data = json.loads(resp.get_data(as_text=True))
    assert 'message' in data



# method erros
def test_post_users(api):
    resp = api.delete('/auth/users')
    assert resp.status == '405 METHOD NOT ALLOWED'

def test_get_new_listing(api):
    resp = api.get('/auth/new-listing')
    assert resp.status == '405 METHOD NOT ALLOWED'

def test_get_register(api):
    resp = api.get('/auth/register')
    assert resp.status == '405 METHOD NOT ALLOWED'

def test_get_new_listing(api):
    resp = api.get('/auth/create-swap')
    assert resp.status == '405 METHOD NOT ALLOWED' 

def test_post_offers(api):
    resp = api.post('/auth/offers')
    assert resp.status == '405 METHOD NOT ALLOWED'