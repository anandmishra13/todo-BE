#!/usr/bin/env bash
# exit on error
set -e

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

