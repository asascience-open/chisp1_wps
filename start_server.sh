#!/bin/bash
python manage.py run_gunicorn -k sync -b 127.0.0.1:8000 &
