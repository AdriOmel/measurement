import db
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route("/")
def hello():
  return "Hello World!"
  
@app.route("/update", methods = ["POST"])
def record_data():
  content = request.json
  sensor = db.check_sensor(content['mac'], content['type'])
  if not sensor:
    sensor = db.add_sensor(content['mac'], content['type'])
  sensor = sensor[0]
  result = db.add_measurements(sensor['id'], content['sensor_value'], sensor['correction'])
  return jsonify(result), 201

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 8080)
