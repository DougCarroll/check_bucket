import requests
from flask import Flask

r = requests.get('https://google.com')
print(r.status_code)
print("This is a speling error")

app = Flask(__name__)

@app.route("/")
def hello():
    return app.send_static_file("index.html")
