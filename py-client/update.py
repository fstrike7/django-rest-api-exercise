import requests

ENDPOINT = "http://127.0.0.1:8000/api/products/2/update/"

data = {
    "title": "Cuaderno modificado", 
    "price": 24
}

res = requests.put(url = ENDPOINT, json=data)
print(res.json())