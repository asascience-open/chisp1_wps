#!/bin/bash
python manage.py run_gunicorn -k gevent --graceful-timeout 120 &
