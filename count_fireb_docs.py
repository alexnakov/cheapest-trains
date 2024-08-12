import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

def print_count_docs_in_collection(collection_name):
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()

    # Count the documents
    doc_count = sum(1 for _ in docs)
    
    # Print the count
    print(f'The collection "{collection_name}" has {doc_count} document(s).')


cred = credentials.Certificate(r"firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
print_count_docs_in_collection('dates_times_n_prices')
