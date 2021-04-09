import requests, json

basePath = 'http://127.0.0.1:80/'

#Change current temperature (0-50)
path0 = basePath + 'dorn/0'
data0 = json.dumps({'value': 18})
requests.put(path0, json=data0)

#Change current light level (0-100)
path1 = basePath + 'dorn/1'
data1 = json.dumps({'value': 90})
requests.put(path1, json=data1)

#Change current heater value (True/False)
path9 = basePath + 'dorn/9'
data9 = json.dumps({'value': True})
requests.put(path9, json=data9)

#Change current height value (1-100)
path10 = basePath + 'dorn/10'
data10 = json.dumps({'value': 90})
requests.put(path10, json=data10)

#Change current tilt value (1-100)
path11 = basePath + 'dorn/11'
data11 = json.dumps({'value': 90})
requests.put(path11, json=data11)

#Get Values
path = basePath + 'dorn/all'
data = requests.get(path).json()
referenceTemperature = data[2]['value']
#etc for any value you need, use the id number of the api

