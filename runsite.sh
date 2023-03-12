#! /bin/bash
export FLASK_APP=papiervoetball.py
flask --debug run
read -s -n 1 -p