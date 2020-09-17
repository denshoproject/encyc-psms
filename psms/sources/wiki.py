import logging
logger = logging.getLogger(__name__)
import os

from bs4 import UnicodeDammit
import mwclient

from django.conf import settings


class MediaWiki():

    def __init__(self):
        self.wiki = _login()

    def exists(self, page_name):
        """Page exists in the wiki.
        """
        page = self.wiki.pages[page_name]
        return page.exists

    def link_exists(self, page_name, target):
        """Check that link exists in page
        """
        page = self.wiki.pages[page_name]
        if target in page.text():
            return True
        return False

    def prepend_text(self, page_name, prependtext):
        """Prepends a string to the existing file text
        """
        page = self.wiki.pages[page_name]
        text = prependtext + page.text()
        response = page.edit(text, 'encyc-psms:psms.sources.prepend_text')
        return response

    def update_text(self, page_name, text):
        """Update existing file text
        """
        logging.debug('update_text(%s, "%s...")' % (page_name, text[:25]))
        page = self.wiki.pages[page_name]
        logging.debug(page)
        response = page.edit(text, 'encyc-psms:psms.sources.update_text')
        logging.debug('response %s' % response)
        return response

    def upload_file(self, abspath, comment='Uploaded by Tansu'):
        """Upload a file
        """
        logging.debug('upload_file(%s)' % abspath)
        page_name = os.path.basename(abspath)
        logging.debug('page_name %s' % page_name)
        wf = self.wiki.images[page_name]
        logging.debug('wf %s' % wf)
        with open(abspath, 'rb') as f:
            logging.debug('f %s' % f)
            response = self.wiki.upload(
                file=f,
                filename=os.path.basename(abspath),
                description='',
                comment=comment,
            )
        logging.debug('response %s' % response)
        return response

    def delete_file(self, page_name, reason):
        """Delete file
        NOTE: requires user with sysop perms
        """
        logging.debug('delete_file(%s, %s)' % (page_name, reason))
        page = self.wiki.pages[page_name]
        logging.debug(page)
        response = page.delete(reason=reason)
        logging.debug('response %s' % response)
        return response


def _login():
    """Get an initialconnection to the wiki.
    """
    logging.debug('initializing')
    if settings.MEDIAWIKI_HTTP_USERNAME and settings.MEDIAWIKI_HTTP_PASSWORD:
        logging.debug('http passwd')
        wiki = mwclient.Site(
            host=settings.MEDIAWIKI_HOST,
            scheme=settings.MEDIAWIKI_SCHEME,
            path='/',
            httpauth=(
                settings.MEDIAWIKI_HTTP_USERNAME,
                settings.MEDIAWIKI_HTTP_PASSWORD
            ),
            retry_timeout=5, max_retries=3,
        )
    else:
        logging.debug('no http passwd')
        wiki = mwclient.Site(
            host=settings.MEDIAWIKI_HOST,
            scheme=settings.MEDIAWIKI_SCHEME,
            path='/',
            retry_timeout=5, max_retries=3,
        )
    logging.debug(wiki)
    logging.debug('logging in')
    wiki.login(
        username=settings.MEDIAWIKI_USERNAME,
        password=settings.MEDIAWIKI_PASSWORD
    )
    logging.debug(wiki)
    logging.debug('done')
    return wiki
