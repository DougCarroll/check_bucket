import sys
from flask import Flask
from flask import request
from check_bucket import check_bucket

app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/<bucket>")
def search(bucket):
    # check_bucket was implemented to take arguments from the command line.  So need to pass
    #  an argument list to it
    argList = [bucket]
    results = check_bucket(argList)
    return(str(results))