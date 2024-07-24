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


def get_date_and_time0_as_arrays(data):
    dates_and_prices = []

    for doc_dict in data:
        date_as_obj = datetime.strptime(doc_dict['date'], r'%Y-%m-%d')
        price_float = float(doc_dict['price'][1:])
        dates_and_prices.append([date_as_obj, price_float])

    sorted(dates_and_prices, key=lambda v2: v2[0])

    result_dict = dict()
    for date, price in dates_and_prices:
        if date in result_dict:
            if price < result_dict[date]:
                result_dict[date] = price
        else:
            result_dict[date] = price

    result_array = []
    for key in result_dict:
        result_array.append([datetime.strftime(key, r'%d/%m/%y'), result_dict[key]])

    return result_array

@app.route('/')
def index():
    docs = get_docs_stream() # Same as firebase .stream() method.
    data_of_dicts = docs_to_list_of_dicts(docs)
    data = get_date_and_time0_as_arrays(data_of_dicts)
    data = data[:70]
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)