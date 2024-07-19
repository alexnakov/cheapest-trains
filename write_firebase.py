import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json 

# connect to cloud db
cred = credentials.Certificate(r"firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

with open('data.json','r') as file:
    data_as_list = json.load(file)

batch = db.batch()

for journey in data_as_list:
    data_to_upload = {
        'date': journey[0],
        'time0': journey[1],
        'time1': journey[2],
        'price': journey[3],
    }
    
    doc_ref = db.collection('dates_times_n_prices').document()
    batch.set(doc_ref, data_to_upload)

batch.commit()
