from warnings import catch_warnings
import pytest, json
from ..routes.main import index
from unittest import mock

userId = "0f1dcb48-19a0-11ed-b2a7-704d7b3306bd"

def test_index_get(api):
    resp = api.get('/')
    assert resp.status == '200 OK'

def test_index_get_personal_listings(api):
    resp = api.get('/?user={id}'.format(id = userId))
    assert resp.status == '200 OK'

def test_index_get_filter_results(api):
    resp = api.get('/?category=shirt')
    assert resp.status == '200 OK'

def test_index_get_personal_listings_filtered(api):
    resp = api.get('/?user={id}&category=shirt'.format(id = userId))
    assert resp.status == '200 OK'

def test_index_error(api):
    resp = api.post('/')
    assert resp.status == '405 METHOD NOT ALLOWED'

def test_index_error(api):
    resp = api.delete('/')
    assert resp.status == '405 METHOD NOT ALLOWED'