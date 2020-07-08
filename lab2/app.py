from flask import Flask, render_template
import joblib

app = Flask(__name__)

# Load ML model
model = joblib.load('./notebooks/regr.pkl')

@app.route('/')
def index():

    # Make prediction - features = ['BEDS', 'BATHS', 'SQFT', 'AGE', 'LOTSIZE', 'GARAGE']
    prediction = model.predict([[4, 2.5, 3005, 15, 17903.0, 1]])[0][0].round(1)
    prediction = str(prediction)

    # Return Template
    return render_template("index.html", prediction=prediction)
