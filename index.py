# Flask app for web interface

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup')
def setup():
    return render_template('index.html')

@app.route('/wiki')
def wiki():
    return render_template('index.html')

@app.route('/resources')
def css():
    return 'WIP'