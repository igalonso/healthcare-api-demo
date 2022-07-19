# Google Cloud Healthcare API Demo

This is a simple demo of Healthcare API for Google Cloud. it shows image deidenfication and consent management API.

## Pre installation:

**PRIOR**: Download a DICOM IMAGE that can be deidentified. You can find some here: 

        https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=80969777 

Add it to the main folder of this repo with the name ***1-1-2.dcm***

Also, create a Service Account with the required permissions (Healthcare API, CloudStorage, Translate API, Document AI) and a key. Download and add it to the root folder of this repo.

## Installation: 

To install, run: 

```sh install.sh -g GCP_PROJECT -r GCP_REGION -k KEY_FILE_NAME```

## Run

Run this command:

```sh run.sh```

Open ***site/index.html*** in your browser or run to start the web app.

```open -a "Google Chrome" site/index.html```

