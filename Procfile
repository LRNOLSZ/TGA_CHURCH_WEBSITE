release: python manage.py collectstatic --noinput && python manage.py migrate --noinput && DJANGO_SUPERUSER_PASSWORD=$SUPERUSER_PASSWORD python manage.py createsuperuser --noinput || true
web: gunicorn church_backend.wsgi --log-file -
