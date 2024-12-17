web: gunicorn transaction_system.wsgi --log-file -
worker: celery -A transaction_system worker --loglevel=info
beat: celery -A transaction_system beat --loglevel=info
release: ./manage.py migrate --no-input
