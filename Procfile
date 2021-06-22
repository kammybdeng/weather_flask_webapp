#web: gunicorn app:app
web: gunicorn --host 0.0.0.0 --port ${PORT}
app:app
init: flask db init
migrate: flask db migrate
upgrade: flask db update

