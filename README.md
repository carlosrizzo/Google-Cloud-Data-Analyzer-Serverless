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
 2. From setup path [setup/](setup/) execute:
 ```
 
 export PROJECT_ID=[yout project id]
 export GOOGLE_APPLICATION_CREDENTIALS=[your local path from JSON service account key]
 
 ```
 3. From setup datastore path [setup/datastore/](setup/datastore) execute:
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
