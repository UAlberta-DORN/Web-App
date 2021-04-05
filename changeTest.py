import requests, json

basePath = 'http://127.0.0.1:105/'

#Eg. Change current light level to 100
path1 = basePath + 'dorn/1'
data1 = json.dumps({'value': 100})
requests.put(path1, json=data1)

#Current temperature 
path0 = basePath + 'dorn/0'

#Current heater value (True/False)
path9 = basePath + 'dorn/9'

#Current height value (1-100)
path10 = basePath + 'dorn/10'

#Current tilt value (1-100)
path11 = basePath + 'dorn/11'
