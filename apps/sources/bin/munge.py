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

Problem keyframes:
total_files: 92
missing: 24
['en-denshovh-bpeggie-01.jpg',
 'en-denshovh-yhisaye-01.jpg',
 'en-denshovh-kkara-01.jpg',
 'en-denshovh-tjim-01.jpg',
 'en-denshovh-kben_g-01.jpg',
 'en-denshovh-marchie-02.jpg',
 'en-denshovh-yfrank-01.jpg',
 'en-denshovh-esue-01.jpg',
 'en-denshovh-malfred-01.jpg',
 'en-denshovh-mnorman-01.jpg',
 'en-denshovh-uclifford-01.jpg',
 'en-denshovh-oruth-01.jpg',
 'en-denshovh-ywakako-01.jpg',
 'en-denshovh-kyuri-01.jpg',
 'en-denshovh-droger-01.jpg',
 'en-denshovh-hwilliam-01.jpg',
 'en-denshovh-trudy-02.jpg',
 'en-denshovh-fbob-01.jpg',
 'en-denshovh-ygeorge-01.jpg',
 'en-denshovh-wmasao-01.jpg',
 'en-denshovh-idaniel-01.jpg',
 'en-denshovh-efrank-01.jpg',
 'en-denshovh-hbill-01.jpg',
 'en-denshovh-ffrank-01.jpg',]
problems: 1
['en-denshopd-i226-00003-1.jpg']

"""
from datetime import datetime
import os
import shutil
import sys
from PIL import Image
from django.conf import settings
from sources.models import Source, get_object_upload_path



def resize(src_path, dest_dir, longest_side):
    verified = False
    original_size = None
    resized_size = None
    #
    size = longest_side,longest_side
    src_file = os.path.basename(src_path)
    dest_file = os.path.join(dest_dir, src_file)
    # make dest_dir
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    # make the thumbnail
    im = Image.open(src_path)
    original_size = im.size
    im.thumbnail(size, Image.ANTIALIAS)
    try:
        im.save(dest_file, "JPEG")
        resized_size = im.size
    except:
        pass
    # verify it
    if os.path.exists(dest_file):
        im1 = Image.open(dest_file)
        if im1:
            oversize = False
            for dim in im1.size:
                if dim > longest_side:
                    oversize = True
            if not oversize:
                verified = dest_file
    return verified, original_size, resized_size
    
def munge_photos(source_dir, name):
    """
    Photos
    - thumb: 250px square (maybe try that out to begin with...?)
    - display: 600px x-dim
    - large: 4000px on longest dimension
    """
    start = datetime.now()
    LONGEST_SIDE = 4000
    nonexist = []
    problems = []
    total_files = 0
    n = 0
    source_files = os.listdir(source_dir)
    num_total = len(source_files)
    #
    for fn in source_files:
        n = n + 1
        total_files = total_files + 1
        upload_path = ''
        dest_path = ''
        src_path = ''.join([source_dir, fn])
        eid,ext = os.path.splitext(fn)
        print '%s/%s %s %s' % (n, num_total, name, eid)
        #s = Source.objects.get(encyclopedia_id__contains=eid)
        try:
            s = Source.objects.get(encyclopedia_id__contains=eid)
        except:
            s = None
            nonexist.append(fn)
        # already updated?
        already_updated = False
        if s:
            upload_path = get_object_upload_path(s, fn)
            if upload_path:
                dest_path = ''.join([settings.MEDIA_ROOT, upload_path])
            if dest_path and os.path.exists(dest_path):
                already_updated = True
        if s and not already_updated:
            # OK Go!
            print '  >> %s' % src_path
            print '  >> %s' % s
            upload_path = get_object_upload_path(s, fn)
            dest_path = ''.join([settings.MEDIA_ROOT, upload_path])
            print '  >> %s' % (dest_path)
            dest_dir = os.path.dirname(dest_path)
            print '  >> %s' % (dest_dir)
            # copy (documents)
            if 'pdf' in src_path:
                if src_path and (not os.path.exists(dest_path)):
                    dest_dir = os.path.dirname(dest_path)
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    shutil.copy(src_path, dest_path)
                    print '    >> COPIED'
                if os.path.exists(dest_path) and ((not s.transcript) or (s.transcript != upload_path)):
                    s.original = upload_path
                    s.save()
                    print '    SAVED'
            else:
                # resize
                newfile, orig_size, new_size = resize(src_path, dest_dir, LONGEST_SIDE)
                print '  >> it_worked: %s' % (newfile)
                print '  >> original size: %s' % str(orig_size)
                print '  >> new_size: %s' % str(new_size)
                if newfile:
                    s.original = upload_path
                    s.save()
                    print '    SAVED'
                else:
                    problems.append(fn)
        print
    print 'total_files: %s' % total_files
    print 'missing: %s' % str(len(nonexist))
    print nonexist
    print 'problems: %s' % str(len(problems))
    print problems
    end = datetime.now()
    print 'start:   %s' % start
    print 'end:     %s' % end
    print 'elapsed: %s' % str(end - start)
    

def munge_keyframes(source_dir, name):
    """
    Videos (keyframes)
    - thumb: 250px square
    - display: 640px x - 360px y (HD), 640px x - 480px y (SD)
    """
    LONGEST_SIDE = 640
    ASPECT_RATIOS = {'hd': (640,360),
                     'sd': (640,480),}
    nonexist = []
    source_files = os.listdir(source_dir)
    num_total = len(source_files)
    n = 0
    for fn in source_files:
        n = n + 1
        upload_path = ''
        dest_path = ''
        src_path = ''.join([source_dir, fn])
        eid,ext = os.path.splitext(fn)
        print '%s/%s %s %s' % (n, num_total, name, eid)
        sources = Source.objects.filter(encyclopedia_id__contains=eid)
        if sources:
            for s in sources:
                print '    >> %s' % s
                already_updated = False
                upload_path = get_object_upload_path(s, fn)
                if upload_path:
                    dest_path = ''.join([settings.MEDIA_ROOT, upload_path])
                # OK Go!
                print '         SRC: %s' % src_path
                print '        DEST: %s' % dest_path
                dest_dir = os.path.dirname(dest_path)
                print '              %s' % (dest_dir)
                if src_path and (not os.path.exists(dest_path)):
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    shutil.copy(src_path, dest_path)
                    print '    COPIED'
                if os.path.exists(dest_path) and ((not s.display) or (s.display != upload_path)):
                    s.display = upload_path
                    s.save()
                    print '    SAVED'
        print
    print 'total_files: %s' % num_total
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
            dest_path = ''.join([settings.MEDIA_ROOT, upload_path])
            print '  >> %s' % (upload_path)
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

#munge_photos(     '/var/www/html/ps_masters/PD/',           'pd')
#munge_keyframes(  '/var/www/html/ps_masters/VH/keyframe/',  'vhk')
#munge_transcripts('/var/www/html/ps_masters/VH/transcript/','vht')
