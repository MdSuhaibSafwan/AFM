echo "BUILD START"

python3.9 -m venv venv

echo "created virtualenv"

source venv/bin/activate

echo "activated virtual environment"

pip3 install -r requirements.txt
python3.9 manage.py collectstatic --no-input

echo "Finished"
