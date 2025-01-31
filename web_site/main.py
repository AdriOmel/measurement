import os
import db
from flask import Flask, request, jsonify, render_template, redirect, url_for

MAC = os.environ['MAC_ADDRESS']

app = Flask(__name__)
@app.route("/")
def home():
  sensor_temp = db.check_sensor(MAC, 'temperature')[0]
  sensor_hum = db.check_sensor(MAC, 'humidity')[0]
  return render_template("online_graph.html", sensor_temp=sensor_temp, sensor_hum=sensor_hum, MAC=MAC)


@app.route("/update", methods = ["POST"])
def record_data():
  content = request.json
  sensor = db.check_sensor(content['mac'], content['type'])
  if not sensor:
    sensor = db.add_sensor(content['mac'], content['type'])
  sensor = sensor[0]
  result = db.add_measurements(sensor['id'], content['value'])
  return jsonify(result), 201

@app.route("/sensor/update", methods = ["POST"])
def update_sensor():
  db.update_sensor(request.form['correction'], request.form['sensor_location'], request.form['units'], request.form['id'])
  return redirect(url_for('home'))

@app.route("/measurements/get")
def get_masurements():
  data = db.get_measurements(request.args.get('sensor_type'),  request.args.get('mac_address'))
  last_measurement = data[-1]['sensor_value']
  values = [row['sensor_value'] for row in data]
  labels = [row['datetime'].strftime('%d-%m-%Y %H:%M:%S') for row in data]
  return jsonify({"last_measurement":last_measurement, "values":values, "labels":labels})

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 8080, debug=True)

