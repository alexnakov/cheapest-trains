import pickle

class FirebaseDoc():
    def __init__(self, _data):
        self._data = _data

def fb_collection_generator(list_of_fb_docs):
    for fb_doc in list_of_fb_docs:
        yield fb_doc


with open('sample_data3.pkl','rb') as file:
    list_of_fb_docs = pickle.load(file)