import json

import pytest
import requests

from django.conf import settings
from django.test import Client
from django.urls import reverse


def test_events():
    client = Client()
    response = client.get('/api/2.0/events/')
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data['objects']
    keys = [
        'id','published','start_date','end_date','title','description','url'
    ]
    for o in data['objects']:
        print(o)
        assert isinstance(o, dict)
        for key in keys:
            assert key in o.keys()

def test_locations():
    client = Client()
    response = client.get('/api/2.0/locations/')
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data['objects']
    keys = [
        'uid', 'location_uri', 'lat', 'lng', 'category', 'category_name',
        'location_name', 'title', 'description',
    ]
    for o in data['objects']:
        print(o)
        assert isinstance(o, dict)
        for key in keys:
            assert key in o.keys()
