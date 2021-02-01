from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST', 'PUT'])

def index():
    current = {'lightLevel': 500, 'temperature': 14,
                'vertical':50, 'tilt':69, 'heater':False}
    desired = {'lightLevel': 500, 'temperature': 14,
                'vertical':50, 'tilt':69}
    manual = {'blinds': True, 'heater': False}
    return render_template('index.html', current=current, desired=desired, manual=manual)



app.run(debug = True)