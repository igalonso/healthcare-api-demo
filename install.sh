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
echo "Setting GCP_PROJECT"
CLIENT_EMAIL=$(cat $KEYPATH | jq -r '.client_email')

gcloud auth activate-service-account $CLIENT_EMAIL --key-file=$KEYPATH --project=$GCP_PROJECT
gcloud config set project $GCP_PROJECT
echo "Creating the bucket"
gsutil mb -c standard -l $REGION gs://$BUCKET
gsutil cp 1-1-2.dcm gs://$BUCKET
echo "Enabling Healthcare API"
gcloud services enable healthcare.googleapis.com 
echo "Creating Healthcare Datasets"

gcloud healthcare datasets create $HC_DATASET --location $REGION
gcloud healthcare consent-stores create $CONSENT_DS --dataset=$HC_DATASET --location $REGION
gcloud healthcare dicom-stores create $DICOM --dataset=$HC_DATASET --location $REGION

# # gcloud iam service-accounts create $SVC_ACCOUNT --display-name="Service account for Healthcare API Demo"
# # gcloud iam service-accounts add-iam-policy-binding $SVC_ACCOUNT@$GCP_PROJECT.iam.gserviceaccount.com --member="serviceAccount:$SVC_ACCOUNT@$GCP_PROJECT.iam.gserviceaccount.com" --role='roles/owner'
# # gcloud iam service-accounts keys create key2.json --iam-account=$SVC_ACCOUNT@$GCP_PROJECT.iam.gserviceaccount.com

python3 -m pip install --user virtualenv
# python3 -m venv env
# source env/bin/activate
# pip install -r requirements.txt
cp configuration.ini.template configuration.ini
echo "----> Change the path to your service key in configuration.ini file"
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





