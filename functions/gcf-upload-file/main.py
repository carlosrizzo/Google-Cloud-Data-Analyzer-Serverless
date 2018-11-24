from google.cloud import datastore
from google.cloud import storage
from google.cloud.storage import Blob
from flask import Flask, Response, render_template_string

import os
import google
import hashlib
import json
import time

# Config vars
BUCKET_UPLOADED_FILES = "gcf-uploaded-files"
DS_KIND_UPLOADED = "gcf-uploader-manager"
BUCKET_STATIC_FILES = "gcf-static-files"
TEMPLATE_FILE = "gcf-uploader.html"

def execute(request):
    # Check Method
    if request.method == 'POST':
        # Check Payload
        if not request.files or not 'file' in request.files:
            return ('Bad request: File is required', 400)
               
        try: # Get/Create bucket
            client_storage = storage.Client()
            bucket = client_storage.create_bucket(BUCKET_UPLOADED_FILES)
        except google.api_core.exceptions.Conflict: # Bucket already exists
            bucket = client_storage.get_bucket(BUCKET_UPLOADED_FILES)
        except Exception as e: # Any exception
            return (u'Error: %s' % e, 500) 

        # Get File
        file = request.files.get('file')
        # Buffer
        buff = file.read()
        # Generate File hash
        file_hash = hashlib.md5(buff).hexdigest()
        # Generate path file
        file_path = "%s/%s" % (file_hash, file.filename)

        # Upload file into bucket
        try: 
            blob = Blob(name=file_path, bucket=bucket)
            blob.upload_from_string(buff, content_type=file.content_type)
        except Exception as e: # Any exception
            return (u'Error: %s' % e, 500)

        # Create entity
        try: 
            client_datastore = datastore.Client()
            # Generate Datastore Key
            item_key = client_datastore.key(DS_KIND_UPLOADED, "%s" % (file_hash))
            # Entity
            item = datastore.Entity(key=item_key,)
            item['file_hash'] = file_hash
            item['file_path'] = file_path
            item['file_content_type'] = file.content_type
            item['created_at'] = time.time()
            client_datastore.put(item) 
        except Exception as e: # Any exception
            return (u'Error: %s' % e, 500)

        # Data return
        data = json.dumps({'result' : 'Success', 'filename': file.filename,'hash' : file_hash})
        # Response
        return Response(data, mimetype='application/json')

    # Invalid methods
    elif request.method == 'PUT' or request.method == 'DELETE' or request.method == 'PATCH':
        return (u'Method not allowed', 403)
        
    # Get - Render Template
    else:
        # Get bucket
        try: 
            client_storage = storage.Client()
            bucket = client_storage.get_bucket(BUCKET_STATIC_FILES)
        except Exception as e: # Any exception
            return (u'Error: %s' % e, 500)

        # Get File
        blob = Blob(name=TEMPLATE_FILE, bucket=bucket)
        response = blob.download_as_string()
        # Template vars
        params = {}
        # Render Form
        return render_template_string(response.decode(), **params)