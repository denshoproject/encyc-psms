import os

from bs4 import BeautifulSoup, SoupStrainer, Comment

from django.conf import settings


def all_events():
    xml = open('%s/events/timeline.xml' % settings.MEDIA_ROOT, 'r')
    soup = BeautifulSoup(xml, "xml")
    published = 0
    if ('published' in soup.Timeline.attrs):
        published = 1
    events = []
    for event in soup.find_all('Event'):
        e = {'id': int(event.attrs['id']),
             'published': published,
             'start_date': event.Startdate.attrs['datenormal'],
             'end_date': '',
             'title': '',
             'description': '',
             'url': '',}
        if hasattr(event,'Enddate') and hasattr(event.Enddate,'attrs') \
               and event.Enddate.attrs.get('datenormal'):
            e['end_date'] = event.Enddate.attrs['datenormal']
        if hasattr(event,'Title') and event.Title:
             e['title'] = event.Title.string
        if hasattr(event,'Caption') and event.Caption:
             e['description'] = event.Caption.string
        if hasattr(event,'Link') and event.Link:
             e['url'] = event.Link.string
        events.append(e)
    return events
