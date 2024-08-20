mkey = '$2a$10$MqwuNL0vgxnmqMKZQ4svEeIVKGGx2URsJ7ep2uaRY6tMj14AGgOEi'
bid = '66c49183ad19ca34f8989137'

import requests
url = rf'https://api.jsonbin.io/v3/b/{bid}/latest'
headers = {
  'X-Master-Key': mkey
}

req = requests.get(url, json=None, headers=headers)
data_dict = req.json()['record']

print(data_dict.values())

# for key, val_dict in data_dict:
#     print('date', val_dict['date'])
#     print('time0', val_dict['time0'])
#     print('price', val_dict['price'])
#     print(20*'-')