import db
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
@app.route("/")
def home():
  last_measurement_temp, values_temp, labels_temp = get_data('temperature', 'c0:4e:30:13:68:a8')
  last_measurement_hum, values_hum, labels_hum = get_data('humidity', 'c0:4e:30:13:68:a8')
  return render_template("graph.html", labels_temp=labels_temp, labels_hum=labels_hum, values_temp=values_temp, values_hum=values_hum, last_measurement_temp=last_measurement_temp, last_measurement_hum=last_measurement_hum)
def get_data(sensor_type, mac):
  data = db.get_measurements(sensor_type, mac)
  last_measurement = data[-1]['sensor_value']
  values = [row['sensor_value'] for row in data]
  labels = [row['datetime'].strftime('%d-%m-%Y %H:%M:%S') for row in data]
  return last_measurement, values, labels

@app.route("/update", methods = ["POST"])
def record_data():
  content = request.json
  sensor = db.check_sensor(content['mac'], content['type'])
  if not sensor:
    sensor = db.add_sensor(content['mac'], content['type'])
  sensor = sensor[0]
  result = db.add_measurements(sensor['id'], content['value'], sensor['correction'])
  return jsonify(result), 201

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 8080)
