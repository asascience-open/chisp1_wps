#!/bin/bash
python manage.py run_gunicorn -k sync &
