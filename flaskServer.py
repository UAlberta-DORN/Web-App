from flask import Flask, render_template, redirect, url_for, jsonify, request, abort, json
import requests
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
       {'id': 10, 'header': 'current height value', 'value': 95},
       {'id': 11, 'header': 'current tilt value', 'value': 12}]

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
    data = requests.get("http://127.0.0.1:5000/dorn/all").json()
    current = {'lightLevel':data[1]['value'], 'temperature':data[0]['value'],
                 'heater':data[9]['value'], 'height':data[10]['value'], 'tilt':data[11]['value']}
    reference = {'lightLevel':data[3]['value'], 'temperature':data[2]['value'],
                'height':data[7]['value'], 'tilt':data[8]['value'], 'heater':data[5]['value']}
    manual = {'blinds':data[6]['value'], 'heater':data[4]['value']}
    return render_template('index.html', current=current, reference=reference, manual=manual)

# Change reference light and redirect to index
@app.route('/lightForm', methods=['POST'])
def light():
    if request.method == 'POST':
        result = request.form['refLight']
        data = json.dumps({'value': result})
        requests.put("http://127.0.0.1:5000/dorn/3", json=data)
        return redirect(url_for('index'))

# Change reference temperature and redirect to index
@app.route('/tempForm', methods=['POST'])
def temp():
    if request.method == 'POST':
        result = request.form['refTemp']
        data = json.dumps({'value': result})
        requests.put("http://127.0.0.1:5000/dorn/2", json=data)
        return redirect(url_for('index'))
    
# Change manual blind position and redirect to index
@app.route('/blindsForm', methods=['POST'])
def blinds():
    if request.method == 'POST':
        if request.form.get('manBlinds'):
            value = json.dumps({'value': True})
        else:
            value = json.dumps({'value': False})
        requests.put("http://127.0.0.1:5000/dorn/6", json=value)

        result1 = request.form['manHeight']
        data1 = json.dumps({'value': result1})
        requests.put("http://127.0.0.1:5000/dorn/7", json=data1)
        
        result2 = request.form['manTilt']
        data2 = json.dumps({'value': result2})
        requests.put("http://127.0.0.1:5000/dorn/8", json=data2)
        return redirect(url_for('index'))

# Change manual heater status and redirect to index
@app.route('/heaterForm', methods=['POST'])
def heater():
    if request.method == 'POST':
        if request.form.get('manHeater'):
            value1 = json.dumps({'value': True})
        else:
            value1 = json.dumps({'value': False})
        requests.put("http://127.0.0.1:5000/dorn/4", json=value1)

        if request.form.get('refHeater'):
            value2 = json.dumps({'value': True})
        else:
            value2 = json.dumps({'value': False})
        requests.put("http://127.0.0.1:5000/dorn/5", json=value2)
        return redirect(url_for('index'))   
 
# Render datalogger with requested timeframe
@app.route('/datalogger', methods=['POST'])
def datalogger():
    if request.method == 'POST':
        timeframe = {'date':request.form['requestDate'],
              'time1':request.form['requestTime1'],
              'time2':request.form['requestTime2']}
    return render_template('datalogger.html', timeframe=timeframe)


if __name__ == '__main__':
    app.run(debug=True)