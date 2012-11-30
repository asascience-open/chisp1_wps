#!/bin/bash
kill -9  $(ps aux | grep run_gunicorn | awk '{print $2}') 

