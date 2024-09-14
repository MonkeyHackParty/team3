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


# 指定したユーザの直近5日間の食事を取得する関数
def get_recent_history_by_user_id(user_id):
    user = session.query(Users).get(user_id)
    # ユーザが見つからない場合は空の値を返す
    if user is None:
        return None

    # SQLで日付を指定するための変数を用意
    # start_day: 4日前の日付
    today = datetime.date.today()
    start_day = today - datetime.timedelta(days=4)

    # SQLでいうSELECTとJOIN
    items = session.query(MealDetails, Meals, Foods).join(
        Meals, MealDetails.meal_id == Meals.meal_id
    ).join(
        Foods, MealDetails.food_id == Foods.food_id
    ).filter(
        Meals.date >= start_day, Meals.date <= today
    ).all()

    current_date = None
    food_list = []
    single_food_list = [] # 一回の食事のfood_list

    for i in items:
        meals = i.Meals
        meal_details = i.MealDetails
        foods = i.Foods

        if current_date == None:
            current_date = meals.date

        # print(meals.date, meal_details.food_id, foods.name)

        # TODO ここ読みづらい
        if meals.date != current_date:
            food_list.append({"date": current_date, "meal_id": meals.meal_id, "foods": single_food_list})
            current_date = meals.date
            single_food_list = []

        single_food_list.append(foods)

        # もしiがitemsの最後なら
        if i == items[-1]:
            food_list.append({"date": meals.date, "meal_id": meals.meal_id, "foods": single_food_list})

    return food_list
