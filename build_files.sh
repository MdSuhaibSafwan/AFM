ECHO "BUILD START"

python3.9 -m venv venv

ECHO "created virtualenv"

source venv/bin/activate

ECHO "activated virtual environment"

pip3 install -r requirements.txt
python3.9 manage.py collectstatic --no-input
