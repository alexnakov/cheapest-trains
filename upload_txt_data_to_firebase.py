import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

def clear_collection(collection_name):
    collection_ref = db.collection(collection_name)
    batch_size = 500
    docs = collection_ref.limit(batch_size).stream()

    deleted = 0
    while True:
        for doc in docs:
            doc.reference.delete()
            deleted += 1
            print(f'Deleted document: {doc.id}')

        if deleted < batch_size:
            break
        docs = collection_ref.limit(batch_size).stream()
        
now = datetime.now()

dates = []
times = []
prices = []

# Putting the data into lists to be POSTED
with open('real-data.txt','r') as file:
    hour1 = 0
    for line in file:
        line1 = line.strip()

        hour2 = int(line1[:2])

        if hour2 < hour1:
            now += timedelta(days=1)

        times.append(line1[:5])
        prices.append(line1[-5:])
        dates.append(now.strftime(r'%d/%m/%Y'))

        hour1 = hour2

# connect to cloud db
cred = credentials.Certificate(r"firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# clearing old data
clear_collection('dates_times_n_prices')

batch = db.batch()

# jsonifying and uploading new data
for i in range(len(dates)):
    data_to_upload = {
        'date': dates[i],
        'time0': times[i],
        'price': prices[i]
    }

    doc_ref = db.collection('dates_times_n_prices').document()
    batch.set(doc_ref, data_to_upload)

batch.commit()
