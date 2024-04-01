python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input
cd transcribe_app

gunicorn transcribe_app.wsgi:application --bind 0:8000
