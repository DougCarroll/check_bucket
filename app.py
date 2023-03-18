from flask import Flask
from flask import request
from check_bucket import check_bucket
from utils import toHTMLTable
from utils import toLink
   
app = Flask(__name__)

@app.route("/")
def index():
    bucket = request.args.get("bucket", "")
    if bucket:
        protocol = request.args.get("protocol", "")
        if protocol == "http":
            proto = "-u"
        else:
            proto = "-s"

        argList = [proto,bucket]
        results = check_bucket(argList)
        results = toLink(results)
        return(toHTMLTable(results))
    else:
        return app.send_static_file("index.html")

@app.route("/<bucket>")
def search(bucket):
    # check_bucket was implemented to take arguments from the command line.  So need to pass
    #  an argument list to it
    argList = [bucket]
    results = check_bucket(argList)
    return(toHTMLTable(results))