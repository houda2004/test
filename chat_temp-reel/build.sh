set -o errexite 
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py runserver