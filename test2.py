mkey = '$2a$10$MqwuNL0vgxnmqMKZQ4svEeIVKGGx2URsJ7ep2uaRY6tMj14AGgOEi'

import requests
url = 'https://api.jsonbin.io/v3/b'
headers = {
  'Content-Type': 'application/json',
  'X-Master-Key': mkey
}
data = {
    1: {
        "date":"20/08/2024",
        "time0":"06:00",
        "price":"12.33"
    },
    2: {
        "date":"20/08/2024",
        "time0":"07:00",
        "price":"17.42"
    },
}

req = requests.post(url, json=data, headers=headers)
print(req.text)