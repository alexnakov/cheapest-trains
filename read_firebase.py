import firebase_admin
from firebase_admin import credentials, firestore

# Path to your service account key file
cred = credentials.Certificate('firebase_key.json')

firebase_admin.initialize_app(cred)

db = firestore.client()

# Get all documents in the collection
docs = db.collection('dates_times_n_prices').stream()

# testing purposes
i = 0

for doc in docs:
    print(f'Document ID: {doc.id}')
    print(f'Data: {doc.to_dict()}')

    i += 1
    if i == 5:
        break