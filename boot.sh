#!/bin/sh
source venv/bin/activate
#cd ~/api
exec gunicorn -b :5000 wsgi:app