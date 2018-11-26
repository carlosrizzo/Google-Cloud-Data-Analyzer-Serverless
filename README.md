# Google Cloud Data Analyzer Serverless

This sample demonstrates how to upload a CSV file into Cloud Storage and trigger a Cloud Functions for data analysis.


## Functions Code

* Upload
See file [functions/gcf-upload-file/main.py](functions/gcf-upload-file/main.py) for the code.
The dependencies are listed in [functions/gcf-upload-file/requirements.txt](functions/gcf-upload-file/requirements.txt).

* Download
See file [functions/gcf-download-file/main.py](functions/gcf-download-file/main.py) for the code.
The dependencies are listed in [functions/gcf-download-file/requirements.txt](functions/gcf-download-file/requirements.txt).

* Parser
See file [functions/gcf-parser-file/main.py](functions/gcf-parser-file/main.py) for the code.
The dependencies are listed in [functions/gcf-parser-file/requirements.txt](functions/gcf-parser-file/requirements.txt).


## Trigger rules

The functions triggers on http request and on create new file in specific Bucket.


## Storage and Database Structure

Users upload an file to Storage bucket `gcf-uploaded-files` and save the path and file reference in Cloud Datastorekind `gcf-uploader-manager`.
Data report will be saved in Cloud Datastore `kind gcf-report-manager`.
Downloaded files will be saved in Bucket `gcf-downloaded-files`.

## Setting up the sample

This sample comes with a Function and web-based UI for testing the function. To configure it:

 1. Create a Google Cloud Project using the [Console GCP](https://console.cloud.google.com)
 1. Create billing account [Console Billing](https://console.cloud.google.com/billing/)
 1. Enable the Cloud Functions API [Console Cloud Functions](https://console.cloud.google.com/functions/)
 1. Enable the Cloud Datastore API [Console Cloud Datastore](https://console.cloud.google.com/datastore/)
 1. Enable the Cloud Storage API [Console Cloud Storage](https://console.cloud.google.com/storage/)
 1. Create IAM User with Editor profile [Console Cloud IAM](https://console.cloud.google.com/iam-admin/)
 1. Create and Export Service Account JSON Key [Console Cloud IAM - Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts/)
 
## Deploy and test

To test the sample:
 1. Download and install gcloud command line tool [Console](https://cloud.google.com/sdk/install)
 2. Create a virtualenv python3.7 and from setup path [setup/](setup/) execute:
 ```
 export PROJECT_ID=[yout project id]
 export GOOGLE_APPLICATION_CREDENTIALS=[your local path from JSON service account key]
 python setup.py
 
 ```
 3. From setup/datastore path [setup/datastore/](setup/datastore) execute:
 ```
 gcloud datastore create-indexes index.yaml
 ``` 
 4. From function path [functions/gcf-upload-file/](functions/gcf-upload-file/) execute:
 ```
 export FUNCTION_NAME="gcf-upload-file";
 gcloud beta functions deploy ${FUNCTION_NAME} --entry-point execute --memory 128MB --runtime python37 --trigger-http;
 ```
 5. Return something like that:
```
Deploying function (may take a while - up to 2 minutes)...done.                                                                                                                                            
availableMemoryMb: 128
entryPoint: execute
httpsTrigger:
  url: https://[region]-[project id].cloudfunctions.net/gcf-upload-file
labels:
  deployment-tool: cli-gcloud
name: projects/[project id]/locations/[region]/functions/gcf-upload-file
runtime: python37
serviceAccountEmail: [service account email]
status: ACTIVE
timeout: 60s
updateTime: '2018-11-22T16:05:07Z'
versionId: '1'
```
 6. From function path [functions/gcf-parser-file/](functions/gcf-parser-file/) execute:
 ```
 export FUNCTION_NAME="gcf-parser-file";
 export TRIGGER_BUCKET_NAME="gcf-uploaded-files";
 gcloud beta functions deploy ${FUNCTION_NAME} --entry-point execute --memory 128MB --runtime python37 --trigger-resource ${TRIGGER_BUCKET_NAME} --trigger-event google.storage.object.finalize;
 ```
 7. Return something like that:
```
Deploying function (may take a while - up to 2 minutes)...done.                                                                                                                                            
availableMemoryMb: 128
entryPoint: execute
eventTrigger:
  eventType: google.storage.object.finalize
  failurePolicy: {}
  resource: projects/_/buckets/gcf-uploaded-files
  service: storage.googleapis.com
labels:
  deployment-tool: cli-gcloud
name: projects/[project id]/locations/[region]/functions/gcf-parse-file
runtime: python37
serviceAccountEmail: [service account email]
status: ACTIVE
timeout: 60s
updateTime: '2018-11-22T19:38:44Z'
versionId: '1'
```
 8. From function path [functions/gcf-download-file/](functions/gcf-download-file/) execute:
 ```
 export FUNCTION_NAME="gcf-download-file";
 gcloud beta functions deploy ${FUNCTION_NAME} --entry-point execute --memory 128MB --runtime python37 --trigger-http;
 ```
 9. Return something like that:
```
Deploying function (may take a while - up to 2 minutes)...done.                                                                                                                                            
availableMemoryMb: 128
entryPoint: execute
httpsTrigger:
  url: https://[region]-[project id].cloudfunctions.net/gcf-download-file
labels:
  deployment-tool: cli-gcloud
name: projects/[project id]/locations/[region]/functions/gcf-download-file
runtime: python37
serviceAccountEmail: [service account email]
status: ACTIVE
timeout: 60s
updateTime: '2018-11-25T13:09:23Z'
versionId: '1'
```
10. Open upload form from url https://[region]-[project id].cloudfunctions.net/gcf-upload-file and submit [static-files/AppleStore.csv](static-files/AppleStore.csv)
11. Return something like that:
```
{"result": "Success", "filename": "AppleStore.csv", "hash": "23be2a238e329154b090c74498d270a8"}
````
12. Open download form from url https://[region]-[project id].cloudfunctions.net/gcf-download-file and select type of download. 
13. Return something like that:
```
[{"id": 284035177, "track_name": "Pandora - Music & Radio", "rating_count_tot": 1126879, "size_bytes": 130242560, "price": 0.0, "prime_genre": "Music"}, {"id": 284993459, "track_name": "Shazam - Discover music, artists, videos & lyrics", "rating_count_tot": 402925, "size_bytes": 147093504, "price": 0.0, "prime_genre": "Music"}, {"id": 290638154, "track_name": "iHeartRadio \u2013 Free Music & Radio Stations", "rating_count_tot": 293228, "size_bytes": 116443136, "price": 0.0, "prime_genre": "Music"}, {"id": 302584613, "track_name": "Kindle \u2013 Read eBooks, Magazines & Textbooks", "rating_count_tot": 252076, "size_bytes": 169747456, "price": 0.0, "prime_genre": "Book"}, {"id": 324684580, "track_name": "Spotify Music", "rating_count_tot": 878563, "size_bytes": 132510720, "price": 0.0, "prime_genre": "Music"}, {"id": 333903271, "track_name": "Twitter", "rating_count_tot": 354058, "size_bytes": 210569216, "price": 0.0, "prime_genre": "News"}, {"id": 336353151, "track_name": "SoundCloud - Music & Audio", "rating_count_tot": 135744, "size_bytes": 105009152, "price": 0.0, "prime_genre": "Music"}, {"id": 418987775, "track_name": "TuneIn Radio - MLB NBA Audiobooks Podcasts Music", "rating_count_tot": 110420, "size_bytes": 101735424, "price": 0.0, "prime_genre": "Music"}, {"id": 421254504, "track_name": "Magic Piano by Smule", "rating_count_tot": 131695, "size_bytes": 55030784, "price": 0.0, "prime_genre": "Music"}, {"id": 509993510, "track_name": "Smule Sing!", "rating_count_tot": 119316, "size_bytes": 109940736, "price": 0.0, "prime_genre": "Music"}, {"id": 510855668, "track_name": "Amazon Music", "rating_count_tot": 106235, "size_bytes": 77778944, "price": 0.0, "prime_genre": "Music"}]
````


