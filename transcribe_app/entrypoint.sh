cd /app
python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input

cp -r /app/collected_static/. /backend/static

gunicorn transcribe_app.wsgi:application --bind 0:8000
