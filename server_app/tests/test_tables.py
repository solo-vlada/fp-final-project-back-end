import pytest
from ..models.tables import Clothing, User
from unittest import mock
import json

# def test_add_user(api):
#     """Ensure a new user can be added to the database."""
#     response = api.post(
#         '/users',
#         data=json.dumps(dict(
#             username='michael',
#             email='concept_crew@lap4.com',
#             password='test',
#             location = 'New York'
#         )),
#         content_type='application/json',
#     )
#     data = json.loads(response.data.decode())
#     assert response.status_code == 201
#     assert 'concept_crew@lap4.com was added!' in data['message']
#     assert 'success' in data['status']

def test_clothing_get(api):
    """Ensure a new user can be added to the database."""
    response = api.get('/')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    print(data)
