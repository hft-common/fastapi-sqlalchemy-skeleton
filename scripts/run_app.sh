#/bin/bash

cd /home/tradingadmin/backend

source /home/tradingadmin/venv/bin/activate


gunicorn main:app -c gunicorn-config.py --log-file /tmp/gunicorn-logs --timeout=0 --daemon

