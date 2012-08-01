from django.conf.urls.defaults import url

from tastypie import fields, utils
from tastypie.resources import Resource, ALL, ALL_WITH_RELATIONS

from events.timeline import all_events


class Event(object):
    def __init__(self, **kwargs):
        self.__dict__['_data'] = {}
    
    def __getattr__(self, name):
        return self._data.get(name, None)
    
    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value
    
    def to_dict(self):
        return self._data


class EventResource(Resource):
    id = fields.CharField(attribute='id')
    published = fields.CharField(attribute='published')
    start_date = fields.CharField(attribute='start_date')
    end_date = fields.CharField(attribute='end_date', blank=True, null=True)
    title = fields.CharField(attribute='title', blank=True, null=True)
    description = fields.CharField(attribute='description', blank=True, null=True)
    url = fields.CharField(attribute='url', blank=True, null=True)
    
    class Meta:
        resource_name = 'events'
        allowed_methods = ['get']
    
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        if isinstance(bundle_or_obj, Bundle):
            kwargs['id'] = bundle_or_obj.obj.uid
        else:
            kwargs['id'] = bundle_or_obj.uid
        return kwargs
    
    def get_object_list(self, request):
        results = []
        for e in all_events():
            obj = Event()
            obj.id = e['id']
            obj.published = e['published']
            obj.start_date = e['start_date']
            obj.end_date = e['end_date']
            obj.title = e['title']
            obj.description = e['description']
            obj.url = e['url']
            results.append(obj)
        return results
    
    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        for e in all_events():
            if e['uid'] == kwargs['pk']:
                obj = Event()
                obj.id = e['id']
                obj.published = e['published']
                obj.start_date = e['start_date']
                obj.end_date = e['end_date']
                obj.title = e['title']
                obj.description = e['description']
                obj.url = e['url']
                return obj
        return None
