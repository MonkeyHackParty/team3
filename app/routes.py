from flask import render_template

from app import app
from app.services import get_all_food, get_food_by_id, get_food_by_meal_id, get_history_by_user_id

@app.route("/")
def index():
    foods = get_all_food()
    return render_template("index.html", foods=foods)

@app.route("/daily")
def daily():
#    food_list = get_food_by_meal_id(1)
#    return render_template("daily.html", food_list=food_list)
    history = get_history_by_user_id(1, is_recent=True)
    return render_template("daily.html", history=history)
