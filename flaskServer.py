from flask import Flask, render_template, redirect, url_for, jsonify, request, abort, json
import requests, csv

app = Flask(__name__)

api = [{'id': 0, 'header': 'current temperature', 'value': 22.8},
       {'id': 1, 'header': 'current lighting', 'value': 600},
       {'id': 2, 'header': 'reference temperature', 'value': 25},
       {'id': 3, 'header': 'reference lighting', 'value': 400},
       {'id': 4, 'header': 'manual heater control', 'value': False},
       {'id': 5, 'header': 'manual heater value', 'value': False},
       {'id': 6, 'header': 'manual blind control', 'value': False},
       {'id': 7, 'header': 'manual height value', 'value': 30},
       {'id': 8, 'header': 'manual tilt value', 'value': 45},
       {'id': 9, 'header': 'current heater value', 'value': True},
       {'id': 10, 'header': 'current height value', 'value': 60},
       {'id': 11, 'header': 'current tilt value', 'value': 10}]

basePath = 'http://127.0.0.1:105/'

# To get api in web browser type in http://localhost:105/dorn/all
@app.route('/dorn/all', methods=['GET'])
def api_all():
    return jsonify(api)


# To get id=0 in web browser type in http://localhost:105/dorn/id?=0
@app.route('/dorn/<int:id>', methods=['GET','PUT'])
def api_get(id):
    if request.method == 'GET':
        results = []
        for data in api:
            if data['id'] == id:
                results.append(data)
        if len(results) == 0:
            abort(404)
        return jsonify(results)
    elif request.method == 'PUT':
        new_value = json.loads(request.get_json())
        for i, data in enumerate(api):
            if data['id'] == id:
                api[i]['value'] = new_value['value']
                return jsonify(api[i])
        abort(400)
        
# Render index html with api values
@app.route('/')
def index():
    path = basePath + 'dorn/all'
    data = requests.get(path).json()
    current = {'lightLevel':data[1]['value'], 'temperature':data[0]['value'],
                 'heater':data[9]['value'], 'height':data[10]['value'], 'tilt':data[11]['value']}
    reference = {'lightLevel':data[3]['value'], 'temperature':data[2]['value'],
                'height':data[7]['value'], 'tilt':data[8]['value'], 'heater':data[5]['value']}
    manual = {'blinds':data[6]['value'], 'heater':data[4]['value']}
    return render_template('index.html', current=current, reference=reference, manual=manual)

# Change submitted values and redirect to index
@app.route('/submitForm', methods=['POST'])
def submitForm():
    path2 = basePath + 'dorn/2'
    path3 = basePath + 'dorn/3'
    path4 = basePath + 'dorn/4'
    path5 = basePath + 'dorn/5'
    path6 = basePath + 'dorn/6'
    path7 = basePath + 'dorn/7'
    path8 = basePath + 'dorn/8'
    
    if request.method == 'POST':
        result2 = request.form['refTemp']
        data2 = json.dumps({'value': result2})
        requests.put(path2, json=data2)
        
        result3 = request.form['refLight']
        data3 = json.dumps({'value': result3})
        requests.put(path3, json=data3)
        
        if request.form.get('manHeater'):
            value4 = json.dumps({'value': True})
        else:
            value4 = json.dumps({'value': False})
        requests.put(path4, json=value4)

        if request.form.get('refHeater'):
            value5 = json.dumps({'value': True})
        else:
            value5 = json.dumps({'value': False})
        requests.put(path5, json=value5)
        
        if request.form.get('manBlinds'):
            value6 = json.dumps({'value': True})
        else:
            value6 = json.dumps({'value': False})
        requests.put(path6, json=value6)

        result7 = request.form['manHeight']
        data7 = json.dumps({'value': result7})
        requests.put(path7, json=data7)
        
        result8 = request.form['manTilt']
        data8 = json.dumps({'value': result8})
        requests.put(path8, json=data8)

        return redirect(url_for('index'))

 
# Render datalogger with requested timeframe
@app.route('/datalogger', methods=['POST'])
def datalogger():
    csvFilePath = r'graphData.csv'
    jsonFilePath = r'graphData.json'
    graphPath = basePath + 'graphData'
    date = '2021-02-09'
    time1 = '12:00'
    time2 = '12:15'
    jsonArray = []
    if request.method == 'POST':
        date = request.form['requestDate']
        time1 = request.form['requestTime1']
        time2 = request.form['requestTime2']
    timeframe = {'date':date, 'time1':time1, 'time2':time2}    
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 
        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            if (row['Date'] == date) and (time1 <= row['Time'] <= time2):
                jsonArray.append(row)
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)
    return render_template('datalogger.html', jsonArray=jsonArray, timeframe=timeframe)

@app.route('/graphData')
def graphData():
    jsonContent=[]
    jsonFileObject = open('graphData.json', 'r')
    jsonContent = json.loads(jsonFileObject.read())
    return jsonify(jsonContent)
    


if __name__ == '__main__':
    app.run(port=105, debug=True)
