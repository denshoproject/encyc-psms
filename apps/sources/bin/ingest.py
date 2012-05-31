"""ingest.py - Throwaway script for importing PD Primary Source Metadata.

Cut-and-paste into manage.py shell (use %paste)
"""
files = [('p','PD_PrimarySource_Metadata_20120525.csv'),
         ('v','VH_PrimarySource_Metadata_20120525.csv'),]
def ingest(files):
    import csv
    from sources.models import Source
    MEDIA_FORMATS = {
        'Photo': 'image',
        'Doc': 'document',
        'VH': 'video',
        }
    def normalize_media(media_format):
        if media_format:
            return MEDIA_FORMATS[media_format]
        return ''
    for f,fn in files:
        reader = csv.reader(open(fn, 'rb'), delimiter=',', quotechar='"')
        n = 0
        for row in reader:
            print '%s:%s %s' % (f, n, row[0])
            if n and ('VH_' in fn):
                s = Source(
                    headword = row[0],
                    densho_id = row[1],
                    encyclopedia_id = row[2],
                    aspect_ratio = row[3].lower(),
                    caption = row[4],
                    courtesy = row[5],
                    institution_id = row[6],
                    collection_name = row[7],
                    external_url = row[8],
                    creative_commons = row[9],
                    media_format = normalize_media(row[10]),
                    )
                s.save()
            elif n:
                s = Source(
                    headword = row[0],
                    densho_id = row[1],
                    encyclopedia_id = row[2],
                    caption = row[3],
                    courtesy = row[4],
                    institution_id = row[5],
                    collection_name = row[6],
                    external_url = row[7],
                    creative_commons = row[8],
                    media_format = normalize_media(row[9]),
                    )
                s.save()
            n = n + 1
ingest(files)
