import pickle
from flask import Flask, render_template, url_for
from read_firebase import get_all_data
from generate_sample_data import FirebaseDoc

app = Flask(__name__)

def generate_firebase_stream(pickle_list):
    for doc in pickle_list:
        yield doc

with open('sample_data.pkl','rb') as file:
        loaded_list = pickle.load(file)
        docs = generate_firebase_stream(loaded_list)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)