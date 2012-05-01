"""ingest.py - Throwaway script for importing PD Primary Source Metadata.

Must be run from within manage.py shell.
"""
import csv
from sources.models import Source
fn = '/home/gjost/psms/apps/sources/PD_PrimarySource_Metadata_20120430.csv'
reader = csv.reader(open(fn, 'rb'), delimiter=',', quotechar='"')
n = 0
for row in reader:
    if n:
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
            media_format = row[9],
            )
        s.save()
    n = n + 1
