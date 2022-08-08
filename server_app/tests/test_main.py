from warnings import catch_warnings
import pytest, requests, json
from ..routes.main import index
from unittest import mock

def test_index_get(api):
    resp = api.get('/')
    assert resp.status == '200 OK'
    print(resp.json)

def test_index_post(api):
    resp = api.post('/')
    assert resp.status == '200 OK'
    assert resp.json == {'message': 'added clothing'}

def test_index_error(api):
        resp = api.delete('/')
        assert resp.status == '405 METHOD NOT ALLOWED'
