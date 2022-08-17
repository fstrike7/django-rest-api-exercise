import requests

ENDPOINT = "http://127.0.0.1:8000/api/products/"

res = requests.get(url = ENDPOINT)
print(res.json())