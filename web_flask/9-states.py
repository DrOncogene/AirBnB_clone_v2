#!/usr/bin/python3
"""
display a list of all states grabbed from the db
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception):
    storage.close()


@app.route('/states', strict_slashes=False)
def states_list():
    states = storage.all(State).values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state(id):
    states = storage.all(State)
    key = "State.{}".format(id)
    if key in states:
        return render_template('9-states.html', state=states[key])
    else: 
        return render_template('9-states.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
