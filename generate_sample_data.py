"""
This file is used to generate sample date in the form.

data = [
    [ "2024-07-21","08:04","10:38","\u00a329.25"],
    ["2024-07-21","08:23","11:11","\u00a323.10"],
]

 - About 35 data pts per calendar day
 - beginning hours between 8am and 11:30pm 
 - All journeys 2hrs long
 - Prices between 10 and 90 pounds
"""
import random
from datetime import datetime, timedelta

# GENERATING THE DATA 

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


sample_data = []
date_obj = datetime.now() + timedelta(days=1)

time0 = 8

for j in range(2):
    for i in range(35):
        time0_str = float_to_time_string(time0)
        time1_str = float_to_time_string(time0 + 2.1)
        price = generate_random_price_string()
        sample_data.append([date_obj.strftime(f"%Y-%m-%d"), time0_str, time1_str, price])
        time0 += 0.45

    date_obj = date_obj + timedelta(days=1)
    time0 = 8


# STORING THE DATA AS A JSON FILE.
# import json

# with open('sample_data2.json','w') as file:
#     json_obj = json.dumps(sample_data, indent=2)
#     file.write(json_obj)


# FOR TESTING AND PRINTING PURPOSE

for data in sample_data[:70:7]:
    print(data)

# print(len(sample_data))