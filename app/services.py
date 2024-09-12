from config import session
from app.models import Foods

def get_all_food():
    food = session.query(Foods).all()
    return food

def get_food_by_id(food_id):
    food = session.query(Foods).get(food_id)
    return food
