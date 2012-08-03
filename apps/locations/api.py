from django.conf.urls.defaults import url

from tastypie import fields, utils
from tastypie.resources import Resource, ALL, ALL_WITH_RELATIONS

from locations.facilities import all_facilities


class Location(object):
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
    lat = fields.CharField(attribute='lat')
    lng = fields.CharField(attribute='lng')
    category = fields.CharField(attribute='category')
    nps_name = fields.CharField(attribute='nps_name')
    location_name = fields.CharField(attribute='location_name')
    
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
        for f in all_facilities():
            obj = Location()
            obj.uid = f['uid']
            obj.lat = f['lat']
            obj.lng = f['lng']
            obj.category = f['category']
            obj.nps_name = f['nps_name']
            obj.location_name = f['location_name']
            results.append(obj)
        return results
    
    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        for f in all_facilities():
            if f['uid'] == kwargs['pk']:
                obj = Location()
                obj.uid = f['uid']
                obj.lat = f['lat']
                obj.lng = f['lng']
                obj.category = f['category']
                obj.nps_name = f['nps_name']
                obj.location_name = f['location_name']
                return obj
        return None
