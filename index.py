# Flask app for web interface

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/setup')
def setup():
    return render_template('base.html')

@app.route('/wiki')
def wiki():
    return render_template('base.html')

@app.route('/static/css')
def serve_css():
    return app.send_static_file('css/luminote.css')