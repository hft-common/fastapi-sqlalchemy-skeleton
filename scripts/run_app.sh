#/bin/bash

cd /home/ubuntu/backend

gunicorn -c gunicorn-config.py --log-file /tmp/gunicorn-logs --timeout=0 --daemon

