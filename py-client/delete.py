import requests

ENDPOINT = "http://127.0.0.1:8000/api/products/2/delete/"

res = requests.delete(url = ENDPOINT)
# status_code == 204 significa que el producto fue eliminado correctamente.
print(res.status_code == 204)