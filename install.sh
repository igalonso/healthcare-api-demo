export GCP_PROJECT="healthcare-api-demo-352513"
export HC_DATASET="demo-dataset"
export REGION="europe-west3"
export UUID=$(uuidgen | tr '[:upper:]' '[:lower:]')
export BUCKET="healthcare-gcs-$UUID"
export SVC_ACCOUNT="hc-svc-account"
export KEY_PATH=$(pwd)"/key.json"

gcloud config set project $GCP_PROJECT
gcloud auth login
gsutil mb -c standard -l $REGION gs://$BUCKET
echo "----> You must have an image called 1-1-2.dcm in your folder. You can find some here: https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=80969777"
gsutil cp 1-1-2.dcm gs://$BUCKET
gcloud healthcare datasets create $HC_DATASET --location $REGION
gcloud iam service-accounts create $SVC_ACCOUNT --display-name="Service account for Healthcare API Demo"
gcloud iam service-accounts add-iam-policy-binding $SVC_ACCOUNT@$GCP_PROJECT.iam.gserviceaccount.com --member="serviceAccount:$SVC_ACCOUNT@$GCP_PROJECT.iam.gserviceaccount.com" --role='roles/owner'
gcloud iam service-accounts keys create key2.json --iam-account=$SVC_ACCOUNT@$GCP_PROJECT.iam.gserviceaccount.com

python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
pip install Flask
cp configuration.ini.template configuration.ini
echo "----> Change the path to your service key in configuration.ini file"




