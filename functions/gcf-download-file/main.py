from google.cloud import datastore
from google.cloud import storage
from google.cloud.storage import Blob
from flask import Flask, Response, render_template_string

import os
import hashlib
import json

# Global Vars
PROJECT_ID = os.environ.get('GCP_PROJECT', None)
REGION = os.environ.get('FUNCTION_REGION', None)

# Get env vars
BUCKET_STATIC_FILES = "gcf-static-files"
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
                query = client_datastore.query(kind=DS_KIND_REPORT)
                # Get all itens
                list_itens = query.fetch()
            except Exception as e: # Any exception
                return (u'Error: %s' % e, 500) 
            
            # Response type
            if t == 'JSON':
                response = []
                mime = 'application/json'
                for item in list_itens:
                    response.append({'id' : item['id']
                                    ,'track_name' : item['track_name']
                                    ,'rating_count_tot' : item['rating_count_tot']
                                    ,'size_bytes' : item['size_bytes']
                                    ,'price' : item['price']
                                    ,'prime_genre' : item['prime_genre']})
                response = json.dumps(response)
            else:
                mime = 'text/csv'
                response = "id,track_name,rating_count_tot,size_bytes,price,prime_genre\n"
                for item in list_itens:
                    response = response + "%s,%s,%s,%s,%s,%s\n" % \
                    (item['id'],item['track_name'],item['rating_count_tot'],item['size_bytes'],item['price'],item['prime_genre'])
            # Response                 
            return Response(response, mimetype=mime)   
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
    

    