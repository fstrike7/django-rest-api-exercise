import requests

ENDPOINT = "http://127.0.0.1:8000/api/"

res = requests.post(url = ENDPOINT, json={"title": "Hello World"})
print(res.json())