export FLASK_APP=main.py
export FLASK_ENV=development
export FLASk_DEBUG=True
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
flask run