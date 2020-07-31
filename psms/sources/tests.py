import pytest

#from django.contrib.auth.models import Group, User
#from django.test import Client, TestCase
#from django.urls import reverse
#from django.utils import timezone

#from wikitools.wiki import Wiki
# 
#from sources import wiki
# 
# 
#class SourcesViewsTestCase(TestCase):
#    def test_links(self):
#        resp = self.client.get('/mw/')
#        self.assertEqual(resp.status_code, 200)
# 
# 
#class SourcesWikiTestCase(TestCase):
#    
#    def test_login(self):
#        w = wiki._login()
#        self.assertEqual(type(w), type(Wiki()))
#    
#    def test_exists(self):
#        p = wiki.exists('Articles')
#        self.assertEqual(p, True)
# 
#    def test_upload_file(self):
#        pass
#    def test_prepend_text(self):
#        pass
#    def test_link_exists(self):
#        pass
#    def test_update_text(self):
#        pass
#    def test_delete_file(self):
#        pass
#    def test_replace_file(self):
#        pass
