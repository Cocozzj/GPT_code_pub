import json

import requests

url = "https://gpt-search-za6rvhzkqa-uc.a.run.app/"
headers = {
    "content-type": "application/json"
}
data = {
    "gpt_id": "5kQZdDG0v"
}
response = requests.get(url, headers=headers, json=data)
print("client...", response.text)

