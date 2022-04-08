from ast import If
import json
from flask import Flask
from flask import jsonify
from flask import send_file
from flask import request
from flask_cors import CORS, cross_origin
import configparser
import time
import pydicom
import numpy as np
import png as png
import uuid
import string    
import random
# Imports Python's built-in "os" module
import os
from googleapiclient import discovery
# Imports the google.auth.transport.requests transport
from google.auth.transport import requests

# Imports a module to allow authentication using a service account
from google.oauth2 import service_account



app = Flask(__name__)
CORS(app)


config = configparser.ConfigParser()
config.sections()
config.read('configuration.ini')
config.sections()

dataset = config['DEFAULT']['DataSet']
datasetDeid = config['DEFAULT']['DataSetDeID']

region = config['DEFAULT']['Region']
dataStore_Type = config['DEFAULT']['DataStore_Type']
dataStoreRaw= config['DEFAULT']['DataStoreRaw']

dataStoreConsent= config['DEFAULT']['DataStoreConsent']
bucket = config['DEFAULT']['Bucket']
projectID = config['DEFAULT']['ProjectID']
healthcareUrl = config['DEFAULT']['HealthcareUrl']
studyUID = config['DEFAULT']['StudyUID']
multipartName = config['DEFAULT']['MultipartName']
seriesUID = config['DEFAULT']['SeriesUID']
dcmFileName = config['DEFAULT']['DCMFileName']
instanceUID = config['DEFAULT']['InstanceUID']
serviceAccount = config['DEFAULT']['ServiceAccountFileName']

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=serviceAccount

def dicomweb_search_instance(project_id, location, dataset_id, dicom_store_id):
    """Handles the GET requests specified in DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # dicom_store_id = 'my-dicom-store' # replace with the DICOM store ID
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, location)

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/instances".format(
        url, dataset_id, dicom_store_id
    )

    # Sets required application/dicom+json; charset=utf-8 header on the request
    headers = {"Content-Type": "application/dicom+json; charset=utf-8"}

    response = session.get(dicomweb_path, headers=headers)
    response.raise_for_status()

    instances = response.json()

    print("Instances:")
    print(json.dumps(instances, indent=2))

    return instances
def dicomweb_search_studies(project_id, location, dataset_id, dicom_store_id):
    """Handles the GET requests specified in the DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # dicom_store_id = 'my-dicom-store' # replace with the DICOM store ID
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, location)

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies".format(
        url, dataset_id, dicom_store_id
    )

    # Refine your search by appending DICOM tags to the
    # request in the form of query parameters. This sample
    # searches for studies containing a patient's name.
    params = {"PatientName": "Sally Zhang"}

    response = session.get(dicomweb_path, params=params)

    response.raise_for_status()

    print("Studies found: response is {}".format(response))

    # Uncomment the following lines to process the response as JSON.
    patients = response.json()
    # print('Patients found matching query:')
    # print(json.dumps(patients, indent=2))

    return patients
def dicomweb_retrieve_study(
    project_id, location, dataset_id, dicom_store_id, study_uid
):
    """Handles the GET requests specified in the DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""

    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the parent dataset's ID
    # dicom_store_id = 'my-dicom-store' # replace with the DICOM store ID
    # study_uid = '1.3.6.1.4.1.5062.55.1.227'  # replace with the study UID
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, location)

    dicomweb_path = "{}/datasets/{}/dicomStores/{}/dicomWeb/studies/{}".format(
        url, dataset_id, dicom_store_id, study_uid
    )

    # When specifying the output file, use an extension like ".multipart."
    # Then, parse the downloaded multipart file to get each individual
    # DICOM file.
    file_name = "study.multipart"

    response = session.get(dicomweb_path)

    response.raise_for_status()

    with open(file_name, "wb") as f:
        f.write(response.content)
        print("Retrieved study and saved to {} in current directory".format(file_name))

    return response
def dicomweb_retrieve_instance(
    project_id,
    location,
    dataset_id,
    dicom_store_id,
    study_uid,
    series_uid,
    instance_uid,
):
    """Handles the GET requests specified in the DICOMweb standard.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""
    # Gets credentials from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )
    # Creates a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    # URL to the Cloud Healthcare API endpoint and version
    base_url = "https://healthcare.googleapis.com/v1"

    url = "{}/projects/{}/locations/{}".format(base_url, project_id, location)

    dicom_store_path = "{}/datasets/{}/dicomStores/{}".format(
        url, dataset_id, dicom_store_id
    )

    dicomweb_path = "{}/dicomWeb/studies/{}/series/{}/instances/{}".format(
        dicom_store_path, study_uid, series_uid, instance_uid
    )

    file_name = "instance.dcm"

    # Set the required Accept header on the request
    headers = {"Accept": "application/dicom; transfer-syntax=*"}
    response = session.get(dicomweb_path, headers=headers)
    response.raise_for_status()

    with open(file_name, "wb") as f:
        f.write(response.content)
        print(
            "Retrieved DICOM instance and saved to {} in current directory".format(
                file_name
            )
        )

    return response
def deidentify_dataset(project_id, location,dataset_id, destination_dataset_id):
    """Uses a DICOM tag keeplist to create a new dataset containing
    de-identified DICOM data from the source dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample."""
    # Imports the Google API Discovery Service.
    

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the dataset's location
    # dataset_id = 'my-source-dataset'  # replace with the source dataset's ID
    # destination_dataset_id = 'my-destination-dataset'  # replace with the destination dataset's ID
    source_dataset = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    destination_dataset = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, destination_dataset_id
    )

    body = {
        "destinationDataset": destination_dataset,
        "config": {
            "dicom": {
                "keepList": {
                    "tags": [
                        "Columns",
                        "NumberOfFrames",
                        "PixelRepresentation",
                        "MediaStorageSOPClassUID",
                        "MediaStorageSOPInstanceUID",
                        "Rows",
                        "SamplesPerPixel",
                        "BitsAllocated",
                        "HighBit",
                        "PhotometricInterpretation",
                        "BitsStored",
                        "TransferSyntaxUID",
                        "SOPInstanceUID",
                        "StudyInstanceUID",
                        "SeriesInstanceUID",
                        "PixelData",
                    ]
                }
            },
            "image": {
                "textRedactionMode": "REDACT_SENSITIVE_TEXT"
            }
        },
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .deidentify(sourceDataset=source_dataset, body=body)
    )

    response = request.execute()
    print(
        "Data in dataset {} de-identified."
        "De-identified data written to {}".format(dataset_id, destination_dataset_id)
    )
    return response

# DICOM - JPG
def convert_to_png(file):
    ds = pydicom.dcmread(file)

    shape = ds.pixel_array.shape

    # Convert to float to avoid overflow or underflow losses.
    image_2d = ds.pixel_array.astype(float)

    # Rescaling grey scale between 0-255
    image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

    # Convert to uint
    image_2d_scaled = np.uint8(image_2d_scaled)

    # Write the PNG file
    with open(f'{file.strip(".dcm")}.png', 'wb') as png_file:
        w = png.Writer(shape[1], shape[0], greyscale=True)
        w.write(png_file, image_2d_scaled)
def list_dicom_stores(project_id, location, dataset_id):
    """Lists the DICOM stores in the given dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/dicom
    before running the sample."""

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    dicom_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    dicom_stores = (
        client.projects()
        .locations()
        .datasets()
        .dicomStores()
        .list(parent=dicom_store_parent)
        .execute()
        .get("dicomStores", [])
    )

    for dicom_store in dicom_stores:
        print(dicom_store)

    return dicom_stores
def list_datasets(project_id, location):

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the location of the datasets
    dataset_parent = "projects/{}/locations/{}".format(project_id, location)

    datasets = (
        client.projects()
        .locations()
        .datasets()
        .list(parent=dataset_parent)
        .execute()
        .get("datasets", [])
    )

    for dataset in datasets:
        print(
            "Dataset: {}\nTime zone: {}".format(
                dataset.get("name"), dataset.get("timeZone")
            )
        )

    return datasets


# ROUTES
@app.route("/demo")
def homePage():
    datasets = list_datasets(projectID,region)
    print(datasets)
    pretty_datasets = []
    for d in datasets:
        pretty_datasets.append(d['name'].split("/")[5])
    response = jsonify(pretty_datasets)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/demo/<param_dataset>")
def retireveDatastores(param_dataset):
    datasets = list_dicom_stores(projectID,region,param_dataset)
    print(datasets)
    pretty_datasets = []
    for d in datasets:
        pretty_datasets.append(d['name'].split("/")[7])
    response = jsonify(pretty_datasets)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/demo/<param_dataset>/datastores/<param_datastore>/sample-image")
def retrieveImage(param_dataset,param_datastore):

    json_params = dicomweb_search_instance(projectID,region,param_dataset,param_datastore)
    args = request.args
    print(args)
    if ( bool(args) and args["onlytags"] == "true"):
        response = jsonify(json_params)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Content-Type','application/json')
        return response
    dicomweb_retrieve_instance(projectID,region,param_dataset,param_datastore,json_params[0]['0020000D']['Value'][0],json_params[0]['0020000E']['Value'][0],json_params[0]['00080018']['Value'][0])
    convert_to_png("instance.dcm")
    response = send_file("instance.png",mimetype="image/png")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/demo/<param_dataset>/datastores/<param_datastore>/sample-image/deid")
def deIdandRetrieve(param_dataset,param_datastore):
    
    S = 5  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
    datasetdeid="demo-dataset-deid"+ran
    deidentify_dataset(projectID,region,param_dataset,datasetdeid)
    time.sleep(10)
    json_params = dicomweb_search_instance(projectID,region,datasetdeid,param_datastore)
    dicomweb_retrieve_instance(projectID,region,datasetdeid,param_datastore,json_params[0]['0020000D']['Value'][0],json_params[0]['0020000E']['Value'][0],json_params[0]['00080018']['Value'][0])
    convert_to_png("instance.dcm")
    return send_file("instance.png",mimetype="image/png")

@app.route("/demo/<param_dataset>/datastores/<param_datastore>")
def retrieveAll(param_dataset,param_datastore):
    return jsonify(dicomweb_search_instance(projectID,region,param_dataset,param_datastore))
