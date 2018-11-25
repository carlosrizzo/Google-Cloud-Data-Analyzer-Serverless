from google.cloud import datastore
from google.cloud import storage
from google.cloud.storage import Blob
from io import StringIO

import google
import os
import json
import os
import pandas
import time

# Define params
PROJECT_ID = os.environ.get('GCP_PROJECT', None)
DS_KIND_REPORT = "gcf-report-manager"

def execute(data, context):
    # Get bucket
    try: 
        client_storage = storage.Client()
        bucket = client_storage.get_bucket(data['bucket'])
    except Exception as e: # Any exception
        print(u'Error: %s' % e)

    # Get File
    blob = Blob(name=data['name'], bucket=bucket)
    file = blob.download_as_string().decode()

    # Read File
    df = pandas.read_csv(StringIO(file), sep=',')
    
    # Filter News
    news = df[(df.prime_genre=='News')]
    # Sort News
    news_1 = news[['id','track_name','rating_count_tot','size_bytes','price','prime_genre']].sort_values(by='rating_count_tot', ascending=False)[0:1]
    
    # Filter Music and Book
    music_book = df[(df.prime_genre=='Music') | (df.prime_genre=='Book')]
    music_book_10 = music_book[['id','track_name','rating_count_tot','size_bytes','price','prime_genre']].sort_values(by='rating_count_tot', ascending=False)[0:10]
    
    # Init Datastore Client
    client_datastore = datastore.Client()
    
    # Interate df news
    for idx, row in news_1.iterrows():
        # Generate Datastore Key
        item_key = client_datastore.key(DS_KIND_REPORT, "%s" % (row[id]))
        # Entity
        item = datastore.Entity(key=item_key,)
        item['id'] = row[id]
        item['track_name'] = row[track_name]
        item['rating_count_tot'] = row[rating_count_tot]
        item['size_bytes'] = row[size_bytes]
        item['price'] = row[price]
        item['prime_genre'] = row[prime_genre]
        item['created_at'] = time.time()
        
        # Save and publish item
        try:
            client_datastore.put(item)
        except Exception as e: # Any exception
            print(u'Error: %s' % e)
            
    # Interate df musoc and book
    for idx, row in music_book_10.iterrows():
        # Generate Datastore Key
        item_key = client_datastore.key(DS_KIND_REPORT, "%s" % (row[id]))
        # Entity
        item = datastore.Entity(key=item_key,)
        item['id'] = row[id]
        item['track_name'] = row[track_name]
        item['rating_count_tot'] = row[rating_count_tot]
        item['size_bytes'] = row[size_bytes]
        item['price'] = row[price]
        item['prime_genre'] = row[prime_genre]
        item['created_at'] = time.time()
        
        # Save and publish item
        try:
            client_datastore.put(item)
        except Exception as e: # Any exception
            print(u'Error: %s' % e)
                
    print("Success") 