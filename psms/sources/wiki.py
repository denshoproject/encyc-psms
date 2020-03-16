import logging
logger = logging.getLogger(__name__)
import os

from bs4 import UnicodeDammit
import wikitools

from django.conf import settings


def _login():
    """Get an initialconnection to the wiki.
    """
    logging.debug('logging in')
    wiki = wikitools.wiki.Wiki(settings.PSMS_MEDIAWIKI_API)
    logging.debug(wiki)
    wiki.login(username=settings.PSMS_MEDIAWIKI_USERNAME,
               password=settings.PSMS_MEDIAWIKI_PASSWORD)
    logging.debug(wiki)
    logging.debug('done')
    return wiki

def exists(page_name):
    """Page exists in the wiki.
    """
    wiki = _login()
    p = wikitools.page.Page(wiki, page_name)
    return p.exists

def link_exists(page_name, target):
    """Check that link exists in page
    """
    wiki = _login()
    p = wikitools.page.Page(wiki, page_name)
    text = UnicodeDammit(p.getWikiText(), smart_quotes_to="html").unicode_markup
    if target in text:
        return True
    return False

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
    logging.debug('update_text(%s, "%s...")' % (page_name, text[:25]))
    wiki = _login()
    p = wikitools.page.Page(wiki, page_name)
    logging.debug(p)
    response = p.edit(text=text)
    logging.debug('response %s' % response)
    return response

def upload_file(abspath, comment='Uploaded by Tansu'):
    """Upload a file
    
    //TODO What to do with previously deleted files?
    
    >>> fn = '/home/gjost/img/6a00e55055.jpg'
    >>> f = open(fn, 'r')
    >>> page_name = '6a00e55055.jpg'
    >>> wf = wikitools.wikifile.File(wiki, page_name)
    >>> wf.upload(f, comment='not much to say about this file...')
    """
    logging.debug('upload_file(%s)' % abspath)
    page_name = os.path.basename(abspath)
    logging.debug('page_name %s' % page_name)
    wiki = _login()
    wf = wikitools.wikifile.File(wiki, page_name)
    logging.debug('wf %s' % wf)
    with open(abspath, 'r') as f:
        logging.debug('f %s' % f)
        response = wf.upload(f, comment=comment, ignorewarnings=True)
    logging.debug('response %s' % response)
    return response

def delete_file(page_name, reason):
    """Delete file
    
    NOTE: requires user with sysop perms
    
    >>> p = wikitools.page.Page(wiki, 'File:6a00e55055.jpg')
    >>> p.delete(reason='that is all')
    """
    logging.debug('delete_file(%s, %s)' % (page_name, reason))
    wiki = _login()
    p = wikitools.page.Page(wiki, page_name)
    logging.debug(p)
    response = p.delete(reason=reason)
    logging.debug('response %s' % response)
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
