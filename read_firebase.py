import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_all_data():
    data = []
    docs = db.collection('dates_times_n_prices').stream()

    for doc in docs:
        data.append(doc.to_dict())

    return data

def print_some_data():
    docs = db.collection('dates_times_n_prices').stream()
    
    i = 0
    for doc in docs:
        print(doc.__dict__)
        print('-'*40)
        print(doc._data)
        print(type(doc._data))
        i += 1
        if i > 0:
            break

print_some_data()