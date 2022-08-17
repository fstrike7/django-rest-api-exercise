import requests

ENDPOINT = "http://127.0.0.1:8000/api/products/"

data = {
    'title': "Cartuchera"
}

res = requests.post(url = ENDPOINT, json=data)
print(res.json())