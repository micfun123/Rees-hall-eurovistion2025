from flask import Flask, render_template, request, redirect, make_response
from collections import defaultdict
import json

app = Flask(__name__)

countries = ["Norway", "Luxembourg", "Estonia", "Israel", "Lithuania", "Spain", "Ukraine ", "United Kingdom","Austria","Iceland","Latvia","Netherlands","Finland","Italy","Poland","Germany","Greece","Armenia","Malta","Portugal","Denmark","Sweden","France","San Marino","Albania"]


votes = defaultdict(int)
predictions = defaultdict(int)

@app.route("/", methods=["GET", "POST"])
def index():
    voted = request.cookies.get("voted")
    message = None

    if request.method == "POST":
        if voted:
            message = "You've already voted!"
        else:
            v1 = request.form.get("vote1")
            v2 = request.form.get("vote2")
            v3 = request.form.get("vote3")
            pred = request.form.get("prediction")

            if v1 and v2 and v3 and pred:
                votes[v1] += 3
                votes[v2] += 2
                votes[v3] += 1
                predictions[pred] += 1
                message = "Thank you for voting!"
                resp = make_response(redirect("/"))
                resp.set_cookie("voted", "yes", max_age=60*60*24*30)  # 30 days
                return resp

    return render_template("index.html", countries=countries, votes=dict(votes),
                           predictions=dict(predictions), message=message)

if __name__ == "__main__":
    app.run(debug=True)
