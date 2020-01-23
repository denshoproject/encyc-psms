from collections import OrderedDict
import os

from bs4 import BeautifulSoup, SoupStrainer, Comment
from lxml import etree
from pykml.factory import KML_ElementMaker as KML

from django.conf import settings



def all_facilities():
    xml = open('%s/locations/facilities.xml' % settings.MEDIA_ROOT, 'r')
    print xml
    soup = BeautifulSoup(xml, "xml")
    facilities = []
    for facility in soup.find_all('Facility'):
        f = OrderedDict()
        f['uid'] = facility.attrs.get('UID')
        f['location_uri'] = _safe_string(facility.Location.LocationURI)
        f['lat'] = _safe_string(facility.Location.GISInfo.GISLat)
        f['lng'] = _safe_string(facility.Location.GISInfo.GISLong)
        f['category'] = facility.Category.attrs.get('code')
        f['category_name'] = _safe_string(facility.Category)
        f['location_name'] = _safe_string(facility.Location.LocationName)
        f['title'] = _safe_string(facility.Name.DenshoName)
        f['description'] = _safe_string(facility.Location.Description)
        facilities.append(f)
    return facilities

def _safe_string(tag):
    try:
        return tag.string
    except AttributeError:
        return ''

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
