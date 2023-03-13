#! /bin/bash
export FLASK_APP=papiervoetbal.py
flask --debug run
read -s -n 1 -p