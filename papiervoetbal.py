from flask import Flask, render_template, redirect, session
import logging
from flask_session import Session
from game import Game, edges

### SETUP ### Copied from an old project
app=Flask(__name__)
app.config.from_object(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = open('SECRET_KEY', 'r').read()
Session(app)
app.logger.setLevel(logging.INFO)

@app.route('/')
def hello():
    # We load the board that corresponds to this user (laugh at him)
    luigiBoard = session.get('game', None)
    if luigiBoard is None: # If there is no board, we create one
        luigiBoard = Game()
        session['game'] = luigiBoard

    disabledButtons = []
    for direction in range(9):
        if not luigiBoard.board.canKickBall(edges[int(direction / 3)][direction % 3]):
            disabledButtons.append(direction)
    
    # Board renderer
    return render_template("board.html", boardMap=luigiBoard.boardAsList(), disabledButtons=disabledButtons)

@app.route('/move/<int:direction>')
def move1(direction):
    # Obligatory board fetching and existence checking
    luigi = session.get('game', None)
    if luigi is None: return redirect('/')
    if luigi.board.kickBall(edges[int(direction / 3)][direction % 3]):
        session['game'] = luigi
    # maybe will add an error message if move is impossible later........
    return redirect('/')

@app.route('/reset')
def reset():
    session.pop('game')
    return redirect('/')
