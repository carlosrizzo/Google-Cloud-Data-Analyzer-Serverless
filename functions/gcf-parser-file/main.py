from google.cloud import pubsub
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
TOPIC_NAME = "gcf-file-process"

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
    
    # Define columns
    x,id,track_name,size_bytes,currency,price, \
    rating_count_tot,rating_count_ver,user_rating, \
    user_rating_ver,ver,cont_rating,prime_genre, \
    sup_devices_num,ipadSc_urls_num,lang_num,vpp_lic = df.columns.values

    # Init Datastore Client
    client_datastore = datastore.Client()
    
    # Init pub sub publisher client
    publisher = pubsub.PublisherClient()
    # Define Topic to publish
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)

    # Interate df
    for idx, row in df.iterrows():
        # Generate Datastore Key
        item_key = client_datastore.key(DS_KIND_REPORT, "%s" % (row[id]))
        # Entity
        item = datastore.Entity(key=item_key,)
        item['id'] = row[id]
        item['track_name'] = row[track_name]
        item['size_bytes'] = row[size_bytes]
        item['currency'] = row[currency]
        item['price'] = row[price]
        item['rating_count_tot'] = row[rating_count_tot]
        item['rating_count_ver'] = row[rating_count_ver]
        item['user_rating'] = row[user_rating]
        item['user_rating_ver'] = row[user_rating_ver]
        item['ver'] = row[ver]
        item['cont_rating'] = row[cont_rating]
        item['prime_genre'] = row[prime_genre]
        item['sup_devices_num'] = row[sup_devices_num]
        item['ipadSc_urls_num'] = row[ipadSc_urls_num]
        item['lang_num'] = row[lang_num]
        item['vpp_lic'] = row[vpp_lic]
        item['created_at'] = time.time()
        
        # Payload queue
        payload = json.dumps(item)
        
        # Save and publish item
        try:
            client_datastore.put(item)
            # Publish
            #publisher.publish(topic_path, payload)
        except Exception as e: # Any exception
            print(u'Error: %s' % e)        
    print("Success") 