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
        facilities.append({
            'uid': facility.attrs['UID'],
            'location_uri': facility.Location.LocationURI.string,
            'lat': facility.Location.GISInfo.GISLat.string,
            'lng': facility.Location.GISInfo.GISLong.string,
            'category': facility.Category.attrs['code'],
            'category_name': facility.Category.string,
            'location_name': facility.Location.LocationName.string,
            'title': facility.Name.DenshoName.string,
            'description': facility.Location.Description.string,})
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
            category = {'fakeid': 1,
                        'code':f['category'],
                        'title': f['category_name'],}
            if category not in categories:
                categories.append(category)
            i = i + 1
    return categories