from google.cloud import datastore
from google.cloud import storage
from google.cloud.storage import Blob
from flask import Flask, Response

import os
import hashlib

# Global Vars
PROJECT_ID = os.environ.get('GCP_PROJECT', None)
REGION = os.environ.get('FUNCTION_REGION', None)

# Get env vars
BUCKET_NAME = "gcf-downloaded-files"
DS_KIND_REPORT = "gcf-report-manager"
DS_KIND_DOWNLOADED = "gcf-donwloader-manager"
TEMPLATE_FILE = "gcf-downloader.html"

def execute(request):
    # Check Method
    if request.method == 'GET':
        # GEt file
        t = request.args.get('type', None)
        if t:
            try: # Get bucket
                client_datastore = datastore.Client()
                # Select kind
                query = client.query(kind=DS_KIND_REPORT)
                # Get all itens
                list_itens = query.fetch()
            except Exception as e: # Any exception
                return (u'Error: %s' % e, 500)
                
            # Not found response
            response = 'Item not found'
            mimetype = 'text/plain'
            
            # Response
            return Response(response, mimetype=mimetype)
            
        else:
            # Get bucket
            try: 
                client_storage = storage.Client()
                bucket = client_storage.get_bucket(BUCKET_STATIC_FILES)
            except Exception as e: # Any exception
                return (u'Error: %s' % e, 500)

            # Get Template File
            blob = Blob(name=TEMPLATE_FILE, bucket=bucket)
            response = blob.download_as_string()
            # Template vars
            params = {}
            # Render Form
            return render_template_string(response.decode(), **params)
    # Method not allowed
    return (u'Error: Method not Allowed', 403)
    

    