from django.conf.urls import url

from tastypie import fields, utils
from tastypie.resources import Resource, ALL, ALL_WITH_RELATIONS

from locations import facilities


class Thing(object):
    def __init__(self, **kwargs):
        self.__dict__['_data'] = {}

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data


class LocationResource(Resource):
    uid = fields.CharField(attribute='uid')
    location_uri = fields.CharField(attribute='location_uri')
    lat = fields.CharField(attribute='lat')
    lng = fields.CharField(attribute='lng')
    category = fields.CharField(attribute='category')
    category_name = fields.CharField(attribute='category_name')
    location_name = fields.CharField(attribute='location_name')
    title = fields.CharField(attribute='title')
    description = fields.CharField(attribute='description')
    
    class Meta:
        resource_name = 'locations'
        allowed_methods = ['get']
    
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        if isinstance(bundle_or_obj, Bundle):
            kwargs['uid'] = bundle_or_obj.obj.uid
        else:
            kwargs['uid'] = bundle_or_obj.uid
        return kwargs
    
    def get_object_list(self, request):
        results = []
        for f in facilities.all_facilities():
            obj = Thing()
            obj.uid = f['uid']
            obj.location_uri = f['location_uri']
            obj.lat = f['lat']
            obj.lng = f['lng']
            obj.category = f['category']
            obj.category_name = f['category_name']
            obj.location_name = f['location_name']
            obj.title = f['title']
            obj.description = f['description']
            results.append(obj)
        return results
    
    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        for f in facilities.facilities():
            if f['uid'] == kwargs['pk']:
                obj = Thing()
                obj.uid = f['uid']
                obj.location_uri = f['location_uri']
                obj.lat = f['lat']
                obj.lng = f['lng']
                obj.category = f['category']
                obj.category_name = f['category_name']
                obj.location_name = f['location_name']
                obj.title = f['title']
                obj.description = f['description']
                return obj
        return None


class CategoryResource(Resource):
    fakeid = fields.CharField(attribute='fakeid')
    code = fields.CharField(attribute='code')
    title = fields.CharField(attribute='title')
    
    class Meta:
        resource_name = 'location-categories'
        allowed_methods = ['get']
    
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        if isinstance(bundle_or_obj, Bundle):
            kwargs['fakeid'] = bundle_or_obj.obj.fakeid
        else:
            kwargs['fakeid'] = bundle_or_obj.fakeid
        return kwargs
    
    def get_object_list(self, request):
        results = []
        for c in facilities.categories():
            obj = Thing()
            obj.fakeid = c['fakeid']
            obj.code = c['code']
            obj.title = c['title']
            results.append(obj)
        return results
    
    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        for c in facilities.categories():
            if c['code'] == kwargs['pk']:
                obj = Thing()
                obj.fakeid = c['fakeid']
                obj.code = c['code']
                obj.title = c['title']
                return obj
        return None
