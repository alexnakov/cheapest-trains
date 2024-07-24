"""
This file is used to generate sample date in the form.

sample_data will be a generator with data as objects.

 - About 35 data pts per calendar day
 - beginning hours between 8am and 11:30pm 
 - All journeys 2hrs long
 - Prices between 10 and 90 pounds
"""

import random
from uuid import uuid4
from datetime import datetime, timedelta

# GENERATING THE DATA 
class FirebaseDoc():
    def __init__(self, _data):
        self._data = _data


def float_to_time_string(hours_float):
    """ Converts a float time like 8.25 into its 'HH:mm' format so '08:15' 
        It allows rollovers. E.g. if 25.5 is inputted it returns '01:30'
    """
    hours_float %= 24
    hours = int(hours_float)
    minutes = int((hours_float - hours) * 60)
    time_string = f"{hours:02}:{minutes:02}"
    return time_string

def generate_random_price_string():
    """ Generate a price between £14 and £90 in format £10.00 """
    pounds = random.randint(14, 90) 
    pence = random.randint(10, 99) 
    return f"£{pounds}.{pence}"

date_obj = datetime.now() + timedelta(days=1)
time0 = 8
sample_data = []

for j in range(90):
    for i in range(35):
        date_str = date_obj.strftime(f"%Y-%m-%d")
        time0_str = float_to_time_string(time0)
        time1_str = float_to_time_string(time0 + 2.1)
        price_str = generate_random_price_string()

        sample_data.append(
            FirebaseDoc(_data={"date": date_str, "time0": time0_str, "time1": time1_str, "price": price_str})
        )
        
        time0 += 0.45

    date_obj = date_obj + timedelta(days=1)
    time0 = 8


# STORING THE DATA WITH PICKLE.
import pickle

with open('sample_data.pkl','wb') as file:
    pickle.dump(sample_data, file)

# FOR TESTING AND PRINTING PURPOSE

# for doc in sample_data[:1000:60]:
#     print(doc._data)

# print(len(sample_data))