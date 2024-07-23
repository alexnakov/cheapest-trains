import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)

def get_all_data():
    data = []

    db = firestore.client()
    docs = db.collection('dates_times_n_prices').stream()

    for doc in docs:
        data.append(doc.to_dict())

    return data