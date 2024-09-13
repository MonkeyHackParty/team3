from app.models import Foods, Users, MealDetails, Meals
from config import session
import datetime


# すべての食べ物の情報を取得する関数
def get_all_food():
    food = session.query(Foods).all()
    return food


# 指定したfood_idの食べ物の情報を取得する関数
def get_food_by_id(food_id):
    food = session.query(Foods).get(food_id)
    return food


# 指定したユーザの最近食べた食事を取得する関数
def get_recent_meal(user_id):
    user = session.query(Users).get(user_id)
    # ユーザが見つからない場合は空の値を返す
    if user is None:
        return None

    # SQLで日付を指定するための変数を用意
    # monday: 今週の月曜日の日付 (YYYY-MM-DD)
    # friday: 今週の金曜日の日付 (YYYY-MM-DD)
    today = datetime.date.today()
    day_of_week = today.weekday()

    monday = today - datetime.timedelta(days=day_of_week)
    friday = monday + datetime.timedelta(days=4)

    # SQLでいうSELECTとJOIN
    items = session.query(MealDetails, Meals).filter(
        MealDetails.meal_id == Meals.meal_id
    ).filter(
        Meals.date >= monday, Meals.date <= friday
    ).all()

    # TODO itemsを整形する

    return items
