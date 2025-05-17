from flask import Flask, render_template, request, redirect, make_response
import json
from collections import defaultdict

app = Flask(__name__)

# In-memory store (replace with database for production)
votes = defaultdict(int)
predictions = defaultdict(int)

# List of countries (example)
countries = ["Norway", "Luxembourg", "Estonia", "Israel", "Lithuania", "Spain", "Ukraine ", "United Kingdom","Austria","Iceland","Latvia","Netherlands","Finland","Italy","Poland","Germany","Greece","Armenia","Malta","Portugal","Denmark","Sweden","France","San Marino","Albania"]

@app.route('/')
def index():
    if request.cookies.get('voted'):
        return redirect('/results')
    return render_template('index.html', countries=countries)

@app.route('/vote', methods=['POST'])
def vote():
    if request.cookies.get('voted'):
        return redirect('/results')

    selected = request.form.getlist('votes')
    prediction = request.form.get('prediction')

    if len(selected) != 3 or prediction not in countries:
        return "Invalid vote", 400

    for country in selected:
        votes[country] += 1
    predictions[prediction] += 1

    resp = make_response(redirect('/results'))
    resp.set_cookie('voted', 'true', max_age=60*60*24*365)  # 1 year
    return resp

@app.route('/results')
def results():
    return render_template('results.html', votes=dict(votes), predictions=dict(predictions))

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8595)