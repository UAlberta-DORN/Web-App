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

# Change reference light and redirect to index
@app.route('/lightForm', methods=['POST'])
def light():
    path3 = basePath + 'dorn/3'
    if request.method == 'POST':
        result = request.form['refLight']
        data = json.dumps({'value': result})
        requests.put(path3, json=data)
        return redirect(url_for('index'))

# Change reference temperature and redirect to index
@app.route('/tempForm', methods=['POST'])
def temp():
    path2 = basePath + 'dorn/2'
    if request.method == 'POST':
        result = request.form['refTemp']
        data = json.dumps({'value': result})
        requests.put(path2, json=data)
        return redirect(url_for('index'))
    
# Change manual blind position and redirect to index
@app.route('/blindsForm', methods=['POST'])
def blinds():
    path6 = basePath + 'dorn/6'
    path7 = basePath + 'dorn/7'
    path8 = basePath + 'dorn/8'
    if request.method == 'POST':
        if request.form.get('manBlinds'):
            value = json.dumps({'value': True})
        else:
            value = json.dumps({'value': False})
        requests.put(path6, json=value)

        result1 = request.form['manHeight']
        data1 = json.dumps({'value': result1})
        requests.put(path7, json=data1)
        
        result2 = request.form['manTilt']
        data2 = json.dumps({'value': result2})
        requests.put(path8, json=data2)
        return redirect(url_for('index'))

# Change manual heater status and redirect to index
@app.route('/heaterForm', methods=['POST'])
def heater():
    path4 = basePath + 'dorn/4'
    path5 = basePath + 'dorn/5'
    if request.method == 'POST':
        if request.form.get('manHeater'):
            value1 = json.dumps({'value': True})
        else:
            value1 = json.dumps({'value': False})
        requests.put(path4, json=value1)

        if request.form.get('refHeater'):
            value2 = json.dumps({'value': True})
        else:
            value2 = json.dumps({'value': False})
        requests.put(path5, json=value2)
        return redirect(url_for('index'))   
 
# Render datalogger with requested timeframe
@app.route('/datalogger', methods=['POST'])
def datalogger():
    csvFilePath = r'graphData.csv'
    date = '2021-02-09'
    time1 = '12:00'
    time2 = '12:15'    
    if request.method == 'POST':
        date = request.form['requestDate']
        time1 = request.form['requestTime1']
        time2 = request.form['requestTime2']
    jsonArray = []    
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 
        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            if (row['Date'] == date) and (time1 <= row['Time'] <= time2):
                jsonArray.append(row)        
    return render_template('datalogger.html', jsonArray=jsonArray)


if __name__ == '__main__':
    app.run(port=105, debug=True)
