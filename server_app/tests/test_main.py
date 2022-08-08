# from warnings import catch_warnings
# import pytest, requests, json
# from ..routes.main import index
# from unittest import mock

# def test_index_get(api):
#     resp = api.get('/')
#     assert resp.status == '200 OK'
#     assert resp.json == []

# def test_index_post(api):
#     resp = api.post('/')
#     assert resp.status == '200 OK'
#     assert resp.json == {"message": "Method not allowed"}

# def test_index_error(api):
#         resp = api.delete('/')
#         assert resp.status == '405 METHOD NOT ALLOWED'

# def test_clothing_get(api):
#     resp = api.get('/clothing')
#     assert resp.status == '200 OK'
#     assert resp.json == []

# def test_clothing_error(api):
#     resp = api.post('/clothing')
#     assert resp.status == '200 OK'
#     assert resp.json == {"message": "Method not allowed"}
