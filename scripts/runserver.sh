#!/bin/sh
. /venv/bin/activate
exec python /api_freebible/manage.py runserver 0.0.0.0:8000
