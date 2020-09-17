import factory
import mwclient
import pytest
import requests

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from sources import models
from sources import wiki

USERNAME = 'admin'
PASSWORD = 'admin'
IDSERVICE_API_BASE = 'http://127.0.0.1:8082/api/0.1'

SOURCE_ID = 'ddr-testing-123'

MEDIAWIKI_URL = f'{settings.MEDIAWIKI_SCHEME}://{settings.MEDIAWIKI_HOST}'
MW_OFFLINE_MSG = "Elasticsearch cluster not available."

def mw_offline():
    """Returns True if cannot contact MediaWiki; use to skip tests
    """
    #if DISABLE_SKIP:
    #    return False
    try:
        r = requests.get(MEDIAWIKI_URL, timeout=1)
        if r.status_code == 200:
            return False
    except ConnectionError:
        print(f'ConnectionError for {MEDIAWIKI_URL}')
        return True
    return True


class SourcesWikiTestCase(TestCase):

    @pytest.mark.skipif(mw_offline(), reason=MW_OFFLINE_MSG)
    def test_login(self):
        mw = wiki.MediaWiki()

        w = wiki._login()
        print(w)
        print(type(w))
        self.assertEqual(type(w), mwclient.client.Site)

    @pytest.mark.skipif(mw_offline(), reason=MW_OFFLINE_MSG)
    def test_exists(self):
        mw = wiki.MediaWiki()
        self.assertEqual(mw.exists('Articles'), True)

#    def test_link_exists(self):
#        pass
#    def test_upload_file(self):
#        pass
#    def test_prepend_text(self):
#        pass
#    def test_update_text(self):
#        pass
#    def test_delete_file(self):
#        pass
#    def test_replace_file(self):
#        pass


@pytest.fixture
def create_user(db, django_user_model):
   def make_user(**kwargs):
       kwargs['password'] = PASSWORD
       return django_user_model.objects.create_user(**kwargs)
   return make_user

@pytest.mark.django_db
def test_login(client, create_user):
    admin_user = create_user(
        username=USERNAME, password=PASSWORD, is_staff=1, is_superuser=1
    )
    client.login(username=USERNAME, password=PASSWORD)
    
@pytest.mark.django_db
def test_index(client):
    assert client.get(reverse('sources-index')).status_code == 200

@pytest.mark.django_db
def test_api_index(client):
    assert client.get(reverse('api-index')).status_code == 200

@pytest.mark.django_db
def test_api_sources(client):
    assert client.get(reverse('api-sources')).status_code == 200

@pytest.mark.django_db
def test_api_sources_sitemap(client):
    assert client.get(reverse('sources-sitemap')).status_code == 200

@pytest.mark.django_db
def test_api_sources_export(client):
    assert client.get(reverse('sources-export')).status_code == 200

class SourceFactory(factory.Factory):
    class Meta:
        model = models.Source
    
    published = False
    densho_id = SOURCE_ID
    encyclopedia_id = SOURCE_ID
    headword = 'Testing'
    media_format = 'photo'
    original = factory.django.ImageField(
        filename=f'{SOURCE_ID}.jpg', color='green',
        width=100, height=100, format='JPEG'
    )

@pytest.mark.skipif(mw_offline(), reason=MW_OFFLINE_MSG)
@pytest.mark.django_db
def test_new_source(client, create_user):
    admin_user = create_user(
        username=USERNAME, password=PASSWORD, is_staff=1, is_superuser=1
    )
    client.login(username=USERNAME, password=PASSWORD)
    source = SourceFactory.build()
    source.save()
 
@pytest.mark.skipif(mw_offline(), reason=MW_OFFLINE_MSG)
@pytest.mark.django_db
def test_api_source(client):
    source = SourceFactory.build()
    source.save()
    assert client.get(
        reverse('api-source', args=[SOURCE_ID])
    ).status_code == 200

@pytest.mark.django_db
def test_api_swagger(client):
    assert client.get(reverse('schema-swagger-ui')).status_code == 200

@pytest.mark.django_db
def test_api_swagger_redoc(client):
    assert client.get(reverse('schema-redoc')).status_code == 200
