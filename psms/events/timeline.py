from collections import OrderedDict
import os

from bs4 import BeautifulSoup, SoupStrainer, Comment

from django.conf import settings


def all_events():
    xml = open('%s/events/timeline.xml' % settings.MEDIA_ROOT, 'r')
    soup = BeautifulSoup(xml, "xml")
    published = 0
    if ('published' in soup.Timeline.attrs):
        published = 1
    blink = soup.new_tag('blink')
    events = []
    
    def pretty_contents(tag):
        """return contents of a caption/etc even if contains other tags.
        """
        parts = []
        for part in tag.contents:
            if type(part) == type(blink):
                parts.append(unicode(part))
            else:
                parts.append(part)
        return ''.join(parts)
    
    for event in soup.find_all('Event'):
        e = OrderedDict()
        e['id'] = int(event.attrs['id'])
        e['published'] = published
        e['start_date'] = event.Startdate.attrs['datenormal']
        e['end_date'] = ''
        e['title'] = ''
        e['description'] = ''
        e['url'] = ''
        if hasattr(event,'Enddate') and hasattr(event.Enddate,'attrs') \
               and event.Enddate.attrs.get('datenormal'):
            e['end_date'] = event.Enddate.attrs['datenormal']
        if hasattr(event,'Title') and event.Title:
            e['title'] = event.Title.string
        if hasattr(event,'Caption') and event.Caption:
            e['description'] = pretty_contents(event.Caption)
        if hasattr(event,'Link') and event.Link:
             e['url'] = event.Link.string
        events.append(e)
    return events
