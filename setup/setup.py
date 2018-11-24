from google.oauth2 import service_account
from google.cloud import pubsub
from google.cloud import storage
from google.cloud.storage import Blob

import google
import os

# Get env vars
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', None)
PROJECT_ID = os.environ.get('PROJECT_ID', None)

# Check env vars
if not GOOGLE_APPLICATION_CREDENTIALS or not PROJECT_ID:
    print(u'Export env vars: GOOGLE_APPLICATION_CREDENTIALS, PROJECT_ID')
    exit()

# Create cloud credentials based on key file
cred = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
scoped_credentials = cred.with_scopes(
    ['https://www.googleapis.com/auth/cloud-platform'])

def main():
	# Setup Pub Sub Topic
	topic = setup_pub_sub_topic('gcf-file-process')
	# Setup Storage Buckets
	bucket_uploaded_files = setup_storage_bucket('gcf-uploaded-files')
	bucket_downloaded_files = setup_storage_bucket('gcf-downloaded-files')
	bucket_static_files = setup_storage_bucket('gcf-static-files')
	# Setup static files
	upload_static_files(bucket_static_files, 'gcf-uploader.html')
	upload_static_files(bucket_static_files, 'gcf-downloader.html')
	return None

def setup_pub_sub_topic(topic_name):
	# Publisher Client
	publisher = pubsub.PublisherClient(credentials=scoped_credentials)
	# Topic Path
	topic_path = publisher.topic_path(PROJECT_ID, topic_name)
	# Create Topic
	try:
		topic = publisher.create_topic(topic_path)
		print(u'Info: Topic %s created' % topic_name)
	except google.api_core.exceptions.AlreadyExists as e:
		print(u'Warning: Topic %s already exists' % topic_name)
	except Exception as e:
		print(u'Error: Something is wrong, review code please')
		raise
	# Topic
	print(topic_path)
	return topic_path

def setup_storage_bucket(bucket_name):
	# Storage Client
	client_storage = storage.Client(credentials=scoped_credentials)
	#  Create bucket uploaded-files
	try: 
		bucket = client_storage.create_bucket(bucket_name)
		print(u'Info: Bucket %s created' % bucket_name)
	except google.api_core.exceptions.Conflict: # Bucket already exists
		bucket = client_storage.get_bucket(bucket_name)
		print(u'Warning: Bucket %s already exists' % bucket_name)
	except Exception as e:
		print(u'Error: Something is wrong, review code please')
		raise
	# Resource
	print(bucket)
	return bucket

def upload_static_files(bucket, file_name):
	# Uploader Form
	blob = Blob(name=file_name, bucket=bucket)
	with open(os.path.abspath('../static-files/%s' % file_name), 'rb') as tmp_file:
		blob.upload_from_file(tmp_file)
	# Resource
	print(u'Info: File %s uploaded' % file_name)
	print(blob)

if __name__ == "__main__":
	main()