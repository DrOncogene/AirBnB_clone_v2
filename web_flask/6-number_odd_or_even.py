#!/usr/bin/python3
"""flask app to display C + a passed string"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    '''returns a text'''
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''returns HBNB'''
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text: str):
    return f"C {text.replace('_', ' ')}"


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python', strict_slashes=False)
def python(text='is cool'):
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>', strict_slashes=False)
def is_num(n):
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def is_num_template(n):
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def is_even_or_odd(n):
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
