import os

from bs4 import BeautifulSoup, SoupStrainer, Comment

from django.conf import settings



def all_facilities():
    xml = open('%s/locations/facilities.xml' % settings.MEDIA_ROOT, 'r')
    soup = BeautifulSoup(xml, "xml")
    facilities = []
    for facility in soup.find_all('Facility'):
        f = {'uid': facility.attrs['UID'],
             'category': facility.Category.attrs['code'],
             'category_name': facility.Category.string,
             'nps_name': facility.Name.NPSName.string,
             'location_name': facility.Location.LocationName.string,
             'lat': facility.Location.GISInfo.GISLat.string,
             'lng': facility.Location.GISInfo.GISLong.string,}
        facilities.append(f)
    return facilities
