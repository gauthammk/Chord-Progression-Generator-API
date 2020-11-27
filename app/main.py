from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return "<h1>Testing the brand new Chord Progression Generator!</h1>"
