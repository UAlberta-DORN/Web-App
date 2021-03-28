import requests, json

basePath = 'http://127.0.0.1:105/'

path1 = basePath + 'dorn/1'
data1 = json.dumps({'value': 100})
requests.put(path1, json=data1)