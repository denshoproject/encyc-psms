from collections import OrderedDict
from pathlib import Path

from bs4 import BeautifulSoup, SoupStrainer, Comment

from django.conf import settings


def all_facilities():
    path = Path(settings.VOCABS_ROOT) / 'api/0.2/facilities.xml'
    if not path.exists():
        msg = f'ERROR: {path} is missing. Is densho-vocab installed?'
        raise Exception(msg)
    with path.open('r') as f:
        xml = f.read()
    soup = BeautifulSoup(xml, "xml")
    facilities = []
    for facility in soup.find_all('Facility'):
        f = OrderedDict()
        f['uid'] = facility.attrs['UID']
        f['location_uri'] = facility.Location.LocationURI.string
        f['lat'] = facility.Location.GISInfo.GISLat.string
        f['lng'] = facility.Location.GISInfo.GISLong.string
        f['category'] = facility.Category.attrs['code']
        f['category_name'] = facility.Category.string
        f['location_name'] = facility.Location.LocationName.string
        f['title'] = facility.Name.DenshoName.string
        f['description'] = facility.Location.Description.string
        facilities.append(f)
    return facilities

def some_facilities(category):
    facilities = []
    for f in all_facilities():
        if f['category'] == category:
            facilities.append(f)
    return facilities

def categories():
    categories = []
    i = 0
    for f in all_facilities():
        if f.get('category',None) and f['category']:
            category = OrderedDict()
            category['fakeid'] = 1
            category['code'] = f['category']
            category['title'] = f['category_name']
            if category not in categories:
                categories.append(category)
            i = i + 1
    return categories
