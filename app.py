from flask import Flask, render_template, url_for
from read_firebase import get_all_data
import pickle

class FirebaseDoc():
    def __init__(self, _data):
        self._data = _data


app = Flask(__name__)

@app.route('/')
def index():
    with 

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)