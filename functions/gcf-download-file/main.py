from google.cloud import datastore
from google.cloud import storage
from google.cloud.storage import Blob
from flask import Flask, Response

import os
import hashlib

# Get env vars
BUCKET_NAME = "gcf-downloaded-files"
DS_KIND_REPORT = "gcf-report-manager"
DS_KIND_DOWNLOADED = "gcf-donloader-manager"

def execute(request):
    try: # Get bucket
        client_datastore = datastore.Client()
        # Select kind
        query = client.query(kind=DS_KIND_REPORT)
        # Get all itens
        list_itens = query.fetch()
    except Exception as e: # Any exception
        return (u'Error: %s' % e, 500)

    # Json File
    buff = file_json
    # Generate File hash
    file_hash = hashlib.md5(buff).hexdigest()
    # Generate path file
    file_path = "downloaded-files/%s/%s" % (file_hash, file.filename)

    # Get bucket
    try: 
        client_storage = storage.Client()
        bucket = client_storage.get_bucket(BUCKET_NAME)
    except Exception as e: # Any exception
        return (u'Error: %s' % e, 500)
    
    # Upload report into bucket
    try: 
        blob = Blob(name=file_path, bucket=bucket)
        blob.upload_from_string(buff, content_type=file.content_type)
    except Exception as e: # Any exception
        return (u'Error: %s' % e, 500)

    # Create entity
    try: 
        client_datastore = datastore.Client()
        # Generate Datastore Key
        item_key = client_datastore.key(DS_KIND_DOWNLOADED, "%s" % (file_hash))
        # Entity
        item = datastore.Entity(key=item_key,)
        item['file_hash'] = file_hash
        item['file_path'] = file_path
        item['file_content_type'] = file.content_type
        item['created_at'] = time.time()
        client_datastore.put(item) 
    except Exception as e: # Any exception
        return (u'Error: %s' % e, 500)

    # Not found response
    response = 'Item not found'
    mimetype = 'text/plain'

    # Found item
    if item:
        # Get path file
        path_file = item['file_path']
        # Create encrypt Blob
        blob = Blob(name=path_file, bucket=bucket)
        response = blob.download_as_string()
        mimetype = item['file_content_type']

    # Response
    return Response(response, mimetype=mimetype)