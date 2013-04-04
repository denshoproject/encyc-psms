import os

from bs4 import UnicodeDammit
import wikitools

from django.conf import settings


def _login():
    """Get an initialconnection to the wiki.
    """
    wiki = wikitools.wiki.Wiki(settings.PSMS_MEDIAWIKI_API)
    wiki.login(username=settings.PSMS_MEDIAWIKI_USERNAME,
               password=settings.PSMS_MEDIAWIKI_PASSWORD)
    return wiki


def exists(page_name):
    """Page exists in the wiki.
    """
    wiki = _login()
    p = wikitools.page.Page(wiki, page_name)
    return p.exists


def upload_file(abspath, comment='Uploaded by Tansu'):
    """Upload a file
    
    //TODO What to do with previously deleted files?
    
    >>> fn = '/home/gjost/img/6a00e55055.jpg'
    >>> f = open(fn, 'r')
    >>> page_name = '6a00e55055.jpg'
    >>> wf = wikitools.wikifile.File(wiki, page_name)
    >>> wf.upload(f, comment='not much to say about this file...')
    """
    page_name = os.path.basename(abspath)
    f = open(abspath, 'r')
    wiki = _login()
    wf = wikitools.wikifile.File(wiki, page_name)
    response = wf.upload(f, comment=comment, ignorewarnings=True)
    f.close()
    return response


def prepend_text(page_name, prependtext):
    """Prepends a string to the existing file text
    
    >>> p = wikitools.page.Page(wiki, 'File:6a00e55055.jpg')
    >>> p.edit(prepend='[prepended]')
    {u'edit': {u'newrevid': 178,
               u'newtimestamp': u'2012-03-23T21:20:30Z',
               u'oldrevid': 177,
               u'pageid': 126,
               u'result': u'Success',
               u'title': u'File:6a00e55055.jpg'}}
    """
    wiki = _login()
    p = wikitools.page.Page(wiki, page_name)
    response = p.edit(prependtext=prependtext)
    return response


def link_exists(page_name, target):
    """Check that link exists in page
    """
    wiki = _login()
    p = wikitools.page.Page(wiki, page_name)
    text = UnicodeDammit(p.getWikiText(), smart_quotes_to="html").unicode_markup
    if target in text:
        return True
    return False


def update_text(page_name, text):
    """Update existing file text

    >>> p = wikitools.page.Page(wiki, 'File:6a00e55055.jpg')
    >>> p.edit(text='new description for this file!!!')
    {u'edit': {u'newrevid': 178,
               u'newtimestamp': u'2012-03-23T21:20:30Z',
               u'oldrevid': 177,
               u'pageid': 126,
               u'result': u'Success',
               u'title': u'File:6a00e55055.jpg'}}
    """
    wiki = _login()
    p = wikitools.page.Page(wiki, page_name)
    response = p.edit(text=text)
    return response


def delete_file(page_name, reason):
    """Delete file
    
    NOTE: requires user with sysop perms
    
    >>> p = wikitools.page.Page(wiki, 'File:6a00e55055.jpg')
    >>> p.delete(reason='that is all')
    """
    wiki = _login()
    p = wikitools.page.Page(wiki, page_name)
    response = p.delete(reason=reason)
    return response


def replace_file():
    """Replace existing file
    
    >>> wf = wikitools.wikifile.File(wiki, '6a00e55055.jpg')
    >>> wf.getToken('edit')
    u'2c0a809d3e558b6c4fdd1f7e103889dc+\\'
    >>> fn = '/home/gjost/img/trash80a.jpg'
    >>> f = open(fn, 'r')
    >>> wf.upload(f)
    {u'upload': {u'filekey': u'10g2k5frt2mg.ta25z9.2.jpg',
                 u'result': u'Warning',
                 u'sessionkey': u'10g2k5frt2mg.ta25z9.2.jpg',
                 u'warnings': {u'exists': u'6a00e55055.jpg'}}}
    >>> wf.upload(f, ignorewarnings=True)
    """
    wiki = _login()
    assert False