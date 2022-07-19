export HC_DATASET="demo-dataset"
export UUID=$(uuidgen | tr '[:upper:]' '[:lower:]')
export BUCKET="healthcare-gcs-$UUID"
export SVC_ACCOUNT="hc-svc-account"
export KEYPATH=$(pwd)"/key.json"
export CONSENT_DS="consent-ds"
export DICOM="datastore-ds-raw"
while getopts g:r:k: flag
do
    case "${flag}" in
        g) gcpproject=${OPTARG};;
        r) region=${OPTARG};;
        k) key=${OPTARG};;
    esac
done

export GCP_PROJECT=$gcpproject;
export REGION=$region
export KEYPATH=$(pwd)"/$key"
export KEY=$key

echo $GCP_PROJECT
echo $REGION
echo $KEYPATH

#Setting GCP_PROJECT
echo "1 ----> Setting GCP_PROJECT"
export CLIENT_EMAIL=$(cat $KEYPATH | jq -r '.client_email')
gcloud auth activate-service-account $CLIENT_EMAIL --key-file=$KEYPATH --project=$GCP_PROJECT
gcloud config set project $GCP_PROJECT
echo "2 ----> Creating the bucket"
gsutil mb -c standard -l $REGION gs://$BUCKET
gsutil cp 1-1-2.dcm gs://$BUCKET
echo "3 ----> Enabling Healthcare API and Document AI and translate API"
gcloud services enable healthcare.googleapis.com documentai.googleapis.com translate.googleapis.com
echo "4 ----> Creating Healthcare Datasets"
gcloud healthcare datasets create $HC_DATASET --location $REGION
gcloud projects add-iam-policy-binding $GCP_PROJECT \
    --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com \
    --role=roles/owner
export PROJECT_NUMBER=$(gcloud projects describe $GCP_PROJECT --format json | jq -r '.projectNumber')
gcloud iam service-accounts update \
    service-$PROJECT_NUMBER@gcp-sa-healthcare.iam.gserviceaccount.com \
    --description="Updated SA " \
    --display-name="UPDATED_DISPLAY_NAME" 
echo "5 ----> Creating Dicom and Consent Store"
gcloud healthcare consent-stores create $CONSENT_DS --dataset=$HC_DATASET --location $REGION
gcloud healthcare dicom-stores create $DICOM --dataset=$HC_DATASET --location $REGION
gcloud healthcare dicom-stores import gcs $DICOM \
  --dataset=$HC_DATASET  \
  --location=$REGION \
  --gcs-uri=gs://$BUCKET/1-1-2.dcm
echo "6 ----> Installing virtualenv"
python3 -m pip install --user virtualenv
cp configuration.ini.template configuration.ini
echo "7 ----> Replacing configuration.ini"
#if not mac
sed -i "s/<SC_KEY>/$KEY/" configuration.ini
#if mac
sed -i '' 's/<SC_KEY>/'$KEY'/g' configuration.ini
#if not mac
sed -i "s/<REGION>/$REGION/" configuration.ini
#if mac
sed -i '' 's/<REGION>/'$REGION'/g' configuration.ini
#if not mac
sed -i "s/<BUCKET_WITH_FILE>/$BUCKET/" configuration.ini
#if mac
sed -i '' 's/<BUCKET_WITH_FILE>/'$BUCKET'/g' configuration.ini
#if not mac
sed -i "s/<GCP_PROJECT>/$GCP_PROJECT/" configuration.ini
#if mac
sed -i '' 's/<GCP_PROJECT>/'$GCP_PROJECT'/g' configuration.ini

echo "8. Creating a Document AI Procesor"
export GCLOUDTOKEN=$(gcloud auth print-access-token)

export DOC_AI_PROC=$(curl -H "Authorization: Bearer $GCLOUDTOKEN" -H "Content-Type: application/json" "https://eu-documentai.googleapis.com/v1/projects/$GCP_PROJECT/locations/eu/processors" -X POST -d '{  "name": "procesor-hc-api","displayName": "procesor-hc-api", "type": "OCR_PROCESSOR"}' | jq -r '.name')

FIELDS=$(echo $DOC_AI_PROC | tr "/" "\n")

for field in $FIELDS
do
    OCR_NAME=$field
done
#if not mac
sed -i "s/<OCR_ID>/$OCR_NAME/" configuration.ini
#if mac
sed -i '' 's/<OCR_ID>/'$OCR_NAME'/g' configuration.ini
echo "8 ----> Finished!"
echo "      run:"
echo "          sh run.sh"
echo "      to execute the demo"

