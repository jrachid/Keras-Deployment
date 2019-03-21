# Load libraries
import flask
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model

# Instantiate flask
app = flask.Flask(__name__)
app.config["SECRET_KEY"] = 'mysecretkey'

class DataForm(FlaskForm):
    g1=IntegerField(u"G1: ")
    g2=IntegerField(u"G2: ")
    g3=IntegerField(u"G3: ")
    g4=IntegerField(u"G4: ")
    g5=IntegerField(u"G5: ")
    g6=IntegerField(u"G6: ")
    g7=IntegerField(u"G7: ")
    g8=IntegerField(u"G8: ")
    g9=IntegerField(u"G9: ")
    g10=IntegerField(u"G10: ")
    submit = SubmitField("Predict")

# Redefine the function to use the loading model
def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    keras.backend.get_session().run(tf.local_variables_initializer())
    return auc

# Load the model, and pass in the custom metric function
global graph
graph = tf.get_default_graph()
model = load_model('games.h5', custom_objects={'auc':auc})

# Define a predict function as an endpoint
@app.route("/predict", methods=["GET","POST"])
def predict():
    data = {"success" : False}
    form = DataForm()
    if form.validate_on_submit():
        flask.session["g1"] = form.g1.data
        flask.session["g2"] = form.g2.data
        flask.session["g3"] = form.g3.data
        flask.session["g4"] = form.g4.data
        flask.session["g5"] = form.g5.data
        flask.session["g6"] = form.g6.data
        flask.session["g7"] = form.g7.data
        flask.session["g8"] = form.g8.data
        flask.session["g9"] = form.g9.data
        flask.session["g10"] = form.g10.data

        params = flask.request.form.to_dict(flat=False)
        # params = flask.request.json
        params.pop("csrf_token")
        params.pop("submit")
        print(params)
        if params == None:
            params = flask.request.args

        if params != None:
            x = pd.DataFrame.from_dict(params, orient='index').transpose()
            with graph.as_default():
                data["prediction"] = str(model.predict(x)[0][0])
                data["success"] = True
                flask.session['result'] = data["prediction"]

        return flask.redirect(flask.url_for("index"))
    return flask.render_template("predict.html", form=form)

@app.route("/")
def index():
    return flask.render_template("index.html")

if __name__== "__main__":
    app.run(debug=True)
    