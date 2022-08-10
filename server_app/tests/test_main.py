from warnings import catch_warnings
import pytest, json
from ..routes.main import index
from unittest import mock

def test_index_get(api):
    resp = api.get('/')
    assert resp.status == '200 OK'

def test_index_get_personal_listings(api):
    resp = api.get('/?user=1f4d9382-17ff-11ed-8ac3-704d7b3306bd')
    assert resp.status == '200 OK'

def test_index_get_filter_results(api):
    resp = api.get('/?category=shirt')
    assert resp.status == '200 OK'

def test_index_get_personal_listings_filtered(api):
    resp = api.get('/?user=1f4d9382-17ff-11ed-8ac3-704d7b3306bd&category=shirt')
    assert resp.status == '200 OK'

def test_index_error(api):
    resp = api.post('/')
    assert resp.status == '405 METHOD NOT ALLOWED'

def test_index_error(api):
    resp = api.delete('/')
    assert resp.status == '405 METHOD NOT ALLOWED'