from flask import Flask, request
app = Flask(__name__)
@app.route("/")
def hello():
  return "Hello World!"
  
@app.route("/update", methods = ["POST"])
def record_data():
  content = request.json
  print(content)
  return "", 204

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 8080)
