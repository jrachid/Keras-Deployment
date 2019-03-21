# Load FLASK
import flask
app = flask.Flask(__name__)

# Define a predict function as an endpoint
@app.route("/predict", methods=["GET","POST"])
def predict():
    data = {"sucess": False}

    # Get the request parametes
    params = flask.request.json
    if (params == None):
        params = flask.request.args

    # if parameters are found, echo the msg parameter
    if (params != None):
        data["response"] = params.get("msg")
        data["success"] = True

    # return a response in json format
    return flask.jsonify(data)

app.run(host='0.0.0.0')
