'''
The main file logic for the app that generates, analyzes, and models Monster data.
'''

from base64 import b64decode
import os

from flask import Flask, render_template, request
from pandas import DataFrame

from app.data import Database
from app.graph import chart
from app.machine import Machine
from Fortuna import random_int, random_float
from MonsterLab import Monster

SPRINT = 3
APP = Flask(__name__)
APP.debug = True


@APP.route("/")
def home():
    '''Home page featuring example monster data.'''
    return render_template(
        "home.html",
        sprint=f"Sprint {SPRINT}",
        monster=Monster().to_dict(),
        password=b64decode(b"VGFuZ2VyaW5lIERyZWFt"),
    )


@APP.route("/data")
def data():
    '''Returns the created database.'''
    if SPRINT < 1:
        return render_template("data.html")
    db = Database()
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table()
    )


@APP.route("/view", methods=["GET", "POST"])
def view():
    '''Takes data from database and charts it, X-axis, Y-axis, and Target are drop down choices.'''
    if SPRINT < 2:
        return render_template("view.html")
    db = Database()
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    x_axis = request.values.get("x_axis") or options[1]
    y_axis = request.values.get("y_axis") or options[2]
    target = request.values.get("target") or options[4]
    df = db.dataframe()
    new_df = df[["Name", "Type", "Level", "Rarity", "Damage", "Health", "Energy", "Sanity", "Timestamp"]]
    graph = chart(
        df=new_df,
        x=x_axis,
        y=y_axis,
        target=target,
    ).to_json()
    return render_template(
        "view.html",
        options=options,
        x_axis=x_axis,
        y_axis=y_axis,
        target=target,
        count=db.count(),
        graph=graph
    )


@APP.route("/model", methods=["GET", "POST"])
def model():
    '''
		Takes the data from our database and creates or loads a file, then models it. Can retrain model.
		Displays title, timestamp, prediction, and confidence percentage.
	'''
    if SPRINT < 3:
        return render_template("model.html")
    db = Database()
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    filepath = "model.joblib"
    df = db.dataframe()
    retrain = request.values.get("retrain", type=bool)
    if not os.path.exists(filepath) or retrain:
        machine = Machine(df[options])
        machine.save(filepath)
    else:
        machine = Machine.open(filepath)
    stats = [round(random_float(1, 250), 2) for _ in range(3)]
    level = request.values.get("level", type=int) or random_int(1, 20)
    health = request.values.get("health", type=float) or stats.pop()
    energy = request.values.get("energy", type=float) or stats.pop()
    sanity = request.values.get("sanity", type=float) or stats.pop()
    prediction, confidence = machine(DataFrame(
        [dict(zip(options, (level, health, energy, sanity)))]
    ))
    info = machine.info(machine.name, machine.timestamp)
    return render_template(
        "model.html",
        info=info,
        level=level,
        health=health,
        energy=energy,
        sanity=sanity,
        prediction=prediction,
        confidence=f"{confidence[0]:.2%}"
    )


if __name__ == '__main__':
    APP.run()