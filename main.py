from ast import If
import json
import re
from flask import Flask
from flask import jsonify
from flask import send_file
from flask import request
from flask import flash, redirect, url_for
import configparser
import time
import pydicom
import numpy as np
import png as png
import string    
import random
# Imports Python's built-in "os" module
import os
from googleapiclient import discovery
# Imports the google.auth.transport.requests transport
from google.auth.transport import requests

# Imports a module to allow authentication using a service account
from google.oauth2 import service_account


UPLOAD_FOLDER = '/'
app = Flask(__name__, template_folder='site')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

#Consent env variables
userUUID = config['DEFAULT']['UserUUID']

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
    client = discovery.build(service_name, api_version)
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
def delete_dataset(project_id, location, dataset_id):
    """Deletes a dataset.

    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the dataset's location
    # dataset_id = 'my-dataset'  # replace with your dataset ID
    dataset_name = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    request = client.projects().locations().datasets().delete(name=dataset_name)

    response = request.execute()
    print("Deleted dataset: {}".format(dataset_id))
    return response
def create_consent_store(
    project_id: str, location: str, dataset_id: str, consent_store_id: str
):
    """Creates a new consent store within the parent dataset.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/consent
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    # consent_store_id = 'my-consent-store'  # replace with the consent store's ID
    consent_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .create(parent=consent_store_parent, body={}, consentStoreId=consent_store_id)
    )

    response = request.execute()
    print(f"Created consent store: {consent_store_id}")
    return response
def delete_consent_store(
    project_id: str, location: str, dataset_id: str, consent_store_id: str
):
    """Deletes the specified consent store.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/consent
    before running the sample."""
    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    # consent_store_id = 'my-consent-store'  # replace with the consent store's ID
    consent_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    consent_store_name = "{}/consentStores/{}".format(
        consent_store_parent, consent_store_id
    )

    request = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .delete(name=consent_store_name)
    )

    response = request.execute()
    print("Deleted consent store: {}".format(consent_store_id))
    return response
#CONSENTS:
def list_consent_stores(project_id, location, dataset_id):

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    consent_store_parent = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )

    consent_stores = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .list(parent=consent_store_parent)
        .execute()
        .get("consentStores", [])
    )

    for consent_store in consent_stores:
        print(consent_store)

    return consent_stores
def list_consents(project_id,location,dataset_id,consent_store):

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'  # replace with your GCP project ID
    # location = 'us-central1'  # replace with the parent dataset's location
    # dataset_id = 'my-dataset'  # replace with the consent store's parent dataset ID
    consent_parent = "projects/{}/locations/{}/datasets/{}/consentStores/{}".format(
        project_id, location, dataset_id,consent_store
    )

    consent_stores = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .consents()
        .list(parent=consent_parent)
        .execute()
        .get("consents", [])
    )
    return consent_stores
def create_consent(project_id,location,dataset_id,consent_store):
    api_version = "v1"
    service_name = "healthcare"

    client = discovery.build(service_name, api_version)

    consent_artifact_parent = "projects/{}/locations/{}/datasets/{}/consentStores/{}".format(
        project_id, location, dataset_id,consent_store
    )

    body = {
        "user_id": userUUID,
        "user_signature" : {
            "user_id": userUUID,
            "signature_time": {"seconds": 1649255061 }
        }
    }
    consentsArtifact = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .consentArtifacts()
        .create(parent=consent_artifact_parent,body=body)
        .execute()
    )

    consent_parent = "projects/{}/locations/{}/datasets/{}/consentStores/{}".format(
        project_id, location, dataset_id,consent_store
    )

    body = {
        "user_id": userUUID,
        "policies": [],
        "consent_artifact": consentsArtifact["name"],
        "state": "DRAFT"
    }

    consent = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .consents()
        .create(parent=consent_parent,body=body)
        .execute()
    )

    print (consent)

    return consent
def register_user_mapping(project_id,location,dataset_id,consent_store,user_id,doctor_id):
    api_version = "v1"
    service_name = "healthcare"

    client = discovery.build(service_name, api_version)

    user_data_mapping_artifact_parent = "projects/{}/locations/{}/datasets/{}/consentStores/{}".format(
        project_id, location, dataset_id,consent_store
    )

    body = {
        "user_id": user_id,
        "data_id" : healthcareUrl+"/studies/"+studyUID+"/series/"+studyUID+"/instances/"+instanceUID
    }
    userDataMapping = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .userDataMappings()
        .create(parent=user_data_mapping_artifact_parent,body=body)
        .execute()
    )

    return userDataMapping
def retrieve_user_mappings(project_id,location,dataset_id,consent_store,user_id):
    api_version = "v1"
    service_name = "healthcare"

    client = discovery.build(service_name, api_version)

    user_data_mapping_artifact_parent = "projects/{}/locations/{}/datasets/{}/consentStores/{}".format(
        project_id, location, dataset_id,consent_store
    )
    userDataMapping = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .userDataMappings()
        .list(parent=user_data_mapping_artifact_parent)
        .execute()
        .get("userDataMappings",[])
        
    )
    return userDataMapping
def activate_consent(project_id,location,dataset_id,consent_store):
    api_version = "v1"
    service_name = "healthcare"
    consents = list_consents(project_id,location,dataset_id,consent_store,)
    draft_consents = []
    for consent in consents:
        if(consent["state"] == 'DRAFT'):
            draft_consents.append(consent)
    print(draft_consents[0])
    client = discovery.build(service_name, api_version)

    body = {
        "consent_artifact": draft_consents[0]["consentArtifact"],
        "ttl": "100s"
    }

    activated_consent = (
        client.projects()
        .locations()
        .datasets()
        .consentStores()
        .consents()
        .activate(name=draft_consents[0]['name'],body=body)
        .execute()
    )

    print (activated_consent)
    
    return activated_consent
def retrieveEntitites(project_id,location,file):
    api_version = "v1"
    service_name = "healthcare"
    client = discovery.build(service_name, api_version)
    nlp_parent = "projects/{}/locations/{}/services/nlp".format(
        project_id, location
    )
    document = str(file.read())
    document = document.strip('\n')
    document = document.strip('\b')
    body = {
        "documentContent": document
    }
    print(body)
    entitites = (
        client.projects()
        .locations()
        .services()
        .nlp()
        .analyzeEntities(nlpService=nlp_parent,body=body)
        .execute()
    )
    print(entitites)
    return entitites

# ROUTES
@app.route("/demo")
def homepage():
    return {}
@app.route("/demo/clean-demo")
def deleteAll():
    datasets = list_datasets(projectID, region)
    for dataset in datasets:
        print(dataset['name'].split("/")[5])
        if (dataset['name'].split("/")[5] != "demo-dataset"):
            print(dataset.get("name"))
            print("Deleting Dataset: "+ dataset['name'].split("/")[5])
            delete_dataset(projectID,region,dataset['name'].split("/")[5])
        else:
            delete_consent_store(projectID,region,dataset['name'].split("/")[5],"consent-ds")
            create_consent_store(projectID,region,dataset['name'].split("/")[5],"consent-ds")
    
    return {"result":"clean"}
@app.route("/demo/datasets")
def retrieveDatasets():
    datasets = list_datasets(projectID,region)
    print(datasets)
    pretty_datasets = []
    for d in datasets:
        pretty_datasets.append(d['name'].split("/")[5])
    response = jsonify(pretty_datasets)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route("/demo/datasets/<param_dataset>")
def retireveDatastores(param_dataset):
    datasets = list_dicom_stores(projectID,region,param_dataset)
    print(datasets)
    pretty_datasets = []
    for d in datasets:
        pretty_datasets.append(d['name'].split("/")[7])
    response = jsonify(pretty_datasets)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route("/demo/datasets/<param_dataset>/datastores/<param_datastore>/sample-image")
def retrieveImage(param_dataset,param_datastore):

    json_params = dicomweb_search_instance(projectID,region,param_dataset,param_datastore)
    args = request.args
    print(args)
    index = args.get("image_index")
    if(index is None):
        index = 0
    if ( bool(args) and args["onlytags"] == "true"):
        response = jsonify(json_params)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Content-Type','application/json')
        return response
    dicomweb_retrieve_instance(projectID,region,param_dataset,param_datastore,json_params[index]['0020000D']['Value'][index],json_params[index]['0020000E']['Value'][0],json_params[index]['00080018']['Value'][0])
    convert_to_png("instance.dcm")
    response = send_file("instance.png",mimetype="image/png")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route("/demo/datasets/<param_dataset>/datastores/<param_datastore>/sample-image/deid")
def deIdandRetrieve(param_dataset,param_datastore):
    
    S = 5  # number of characters in the string.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
    datasetdeid="demo-dataset-deid"+ran
    deidentify_dataset(projectID,region,param_dataset,datasetdeid)
    time.sleep(10)
    json_params = dicomweb_search_instance(projectID,region,datasetdeid,param_datastore)
    args = request.args
    index = args.get("image_index")
    if(index is None):
        index = 0
    if ( bool(args) and args["onlytags"] == "true"):
        response = jsonify(json_params)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Content-Type','application/json')
        return response
    dicomweb_retrieve_instance(projectID,region,datasetdeid,param_datastore,json_params[0]['0020000D']['Value'][0],json_params[0]['0020000E']['Value'][0],json_params[0]['00080018']['Value'][0])
    convert_to_png("instance.dcm")
    response = send_file("instance.png",mimetype="image/png")
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type','application/json')
    return response
@app.route("/demo/datasets/<param_dataset>/datastores/<param_datastore>")
def retrieveAll(param_dataset,param_datastore):
    return jsonify(dicomweb_search_instance(projectID,region,param_dataset,param_datastore))
@app.route("/demo/consents/<param_dataset>")
def retrieveAllConsents(param_dataset):
    response = jsonify(list_consents(projectID,region,param_dataset,"consent-ds"))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type','application/json')    
    return response
@app.route("/demo/consents/<param_dataset>/datastores/<param_datastore>/create")
def createConsent(param_dataset,param_datastore):
    response = jsonify(create_consent(projectID,region,param_dataset,param_datastore))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type','application/json')    
    return response
@app.route("/demo/consents/<param_dataset>/datastores/<param_datastore>/consents/activate")
def activateConsent(param_dataset,param_datastore):
    response = jsonify(activate_consent(projectID,region,param_dataset,param_datastore))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type','application/json')    
    return response
@app.route("/demo/consents/<param_dataset>/datastores/<param_datastore>/usermappings/create")
def registerDataMapping(param_dataset,param_datastore):
    response = jsonify(register_user_mapping(projectID,region,param_dataset,param_datastore,userUUID,userUUID))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type','application/json')    
    return response
@app.route("/demo/consents/<param_dataset>/datastores/<param_datastore>/usermappings")
def retrieveUserMappings(param_dataset,param_datastore):
    response = jsonify(retrieve_user_mappings(projectID,region,param_dataset,param_datastore,userUUID))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type','application/json')    
    return response
@app.route("/demo/nlp",methods=['POST'])
def retrieveNLPEntities():
    response = jsonify(retrieveEntitites(projectID,"europe-west4",request.files['file']))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type','application/json') 
    return response

