import pickle
from datetime import datetime, timedelta
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
        data.append(doc._data)
    return data

# this function is NOT finished
def restructure_data_for_templating(data):
    date_format = r'%Y-%m-%d'
    all_dates_from_data = []

    for data_point in data:
        all_dates_from_data.append(data_point['date'])

    all_dates_from_data = [datetime.strptime(date, date_format) for date in all_dates_from_data]
    
    print(len(all_dates_from_data))
    print(all_dates_from_data[0])
    print(data[0])
    print(data[40])

docs = get_docs_stream() # Same as firebase .stream() method.
data = docs_to_list_of_dicts(docs)
restructure_data_for_templating(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)