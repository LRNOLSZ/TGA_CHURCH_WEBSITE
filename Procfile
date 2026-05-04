release: python manage.py collectstatic --noinput && python manage.py migrate --noinput && python manage.py createsuperuser --noinput || true
web: gunicorn church_backend.wsgi --log-file -
