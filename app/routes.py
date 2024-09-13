from flask import render_template

from app import app
from app.services import get_all_food, get_food_by_id


@app.route("/")
def index():
    foods = get_all_food()
    return render_template("index.html", foods=foods)

@app.route("/daily")
def daily():
    foods = get_all_food()
    return render_template("daily.html", foods=foods)