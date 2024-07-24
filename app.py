import pickle
from flask import Flask, render_template, url_for
from read_firebase import get_all_data
from generate_sample_data import FirebaseDoc

app = Flask(__name__)

def generate_firebase_stream(pickle_list):
    for doc in pickle_list:
        yield doc

def get_docs_stream():
    with open('sample_data.pkl','rb') as file:
        loaded_list = pickle.load(file)
        docs = generate_firebase_stream(loaded_list)
        return docs

def docs_to_list_of_dicts(docs):
    data = []
    for doc in docs:
        data.append(docs._data)

@app.route('/')
def index():
    docs = get_docs_stream() # Same as firebase .stream() method.
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)