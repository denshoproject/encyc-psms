"""munge.py - Throwaway script for resizing and placing PS imgs

Everything in its right place.

Cut-and-paste into manage.py shell (use %paste)

First, make sure that all the encyclopedia_ids are actually unique.
Then make destination paths for them
then do some actual image conversion



These photos didn't make it through the first round:
total_files: 388
problems: 9
['en-denshopd-i151-00481-1.jpg',
 'en-denshopd-i149-00016-1.pdf',
 'en-denshopd-p23-00015-1.jpg',
 'en-denshopd-p25-00065-1.jpg',
 'en-denshopd-i37-00717-1.jpg',
 'en-denshopd-i227-00019-1.jpg',
 'en-denshopd-i114-00167-1.jpg',
 'en-denshopd-i236-00005-1.jpg',
 'en-denshopd-i37-00297-1.jpg'
 ]
"""
import os
import shutil
from django.conf import settings
from sources.models import Source, get_object_upload_path

def munge_photos(source_dir, name):
    nonexist = []
    total_files = 0
    for fn in os.listdir(source_dir):
        total_files = total_files + 1
        eid,ext = os.path.splitext(fn)
        print '%s %s' % (name, eid)
        #s = Source.objects.get(encyclopedia_id__contains=eid)
        try:
            s = Source.objects.get(encyclopedia_id__contains=eid)
        except:
            s = None
            nonexist.append(fn)
        if s:
            print '  >> %s' % s
            path = get_object_upload_path(s, fn)
            print '  >> %s' % (path)
        print
    print 'total_files: %s' % total_files
    print 'problems: %s' % str(len(nonexist))
    print nonexist

def munge_keyframes(source_dir, name):
    nonexist = []
    total_files = 0
    for fn in os.listdir(source_dir):
        total_files = total_files + 1
        eid,ext = os.path.splitext(fn)
        print '%s %s' % (name, eid)
        try:
            s = Source.objects.get(encyclopedia_id__contains=eid)
        except:
            s = None
            nonexist.append(fn)
        if s:
            path = get_object_upload_path(s, fn)
            print '  >> %s' % (path)
        print
    print 'total_files: %s' % total_files
    print 'problems: %s' % str(len(nonexist))
    print nonexist

def munge_transcripts(source_dir, name):
    nonexist = []
    total_files = 0
    for fn in os.listdir(source_dir):
        src_path = '/'.join([source_dir,fn])
        total_files = total_files + 1
        eid,ext = os.path.splitext(fn)
        print '%s %s' % (name, eid)
        try:
            s = Source.objects.get(encyclopedia_id__contains=eid)
        except:
            s = None
            nonexist.append(fn)
        if s:
            upload_path = get_object_upload_path(s, fn)
            print '  >> %s' % (upload_path)
            dest_path = ''.join([settings.MEDIA_ROOT, upload_path])
            print '     %s' % (dest_path)
            if src_path and (not os.path.exists(dest_path)):
                dest_dir = os.path.dirname(dest_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                shutil.copy(src_path, dest_path)
                print '    COPIED'
            if os.path.exists(dest_path) and ((not s.transcript) or (s.transcript != upload_path)):
                s.transcript = upload_path
                s.save()
                print '    SAVED'
        print
    print 'total_files: %s' % total_files
    print 'problems: %s' % str(len(nonexist))
    print nonexist

#munge_photos(     '/home/gjost/ps_masters/PD',           'pd')
#munge_keyframes(  '/home/gjost/ps_masters/VH/keyframe',  'vhk')
munge_transcripts('/home/gjost/ps_masters/VH/transcript','vht')
