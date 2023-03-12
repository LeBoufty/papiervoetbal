from flask import Flask, render_template, redirect, session
import logging
from flask_session import Session


### SETUP ### Copied from an old project
app=Flask(__name__)
app.config.from_object(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = open('SECRET_KEY', 'r').read()
Session(app)
app.logger.setLevel(logging.INFO)

@app.route('/')
def hello():
    return "yippee"