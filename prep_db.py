from datetime import datetime

import app.models
from app.models import Foods, MealDetails, Meals, Users
from config import session

# テーブルの作成
app.models.create_table()

# foodsテーブルにfoods.csvからのデータをいれる
print("\n=== foods ===")
is_first_line = True
with open("foods.csv", mode="r", encoding="utf-8") as f:
    for line in f:
        if is_first_line:
            is_first_line = False
            continue

        # rstrip()で改行コードの削除
        line = line.rstrip()
        items = line.split(",")

        # もっといい書き方があるはず
        food_id = int(items[0])
        name = items[1]
        name_english = items[2]
        category = items[3]
        price = int(items[4])
        energy = int(items[5])
        protein = float(items[6])
        fat = float(items[7])
        carbohydrates = float(items[8])
        salt = float(items[9])
        calcium = int(items[10])
        vegetable = int(items[11])
        iron = float(items[12])
        vitamin_a = int(items[13])
        vitamin_b1 = float(items[14])
        vitamin_b2 = float(items[15])
        vitamin_c = int(items[16])
        place_of_origin = items[17]
        allergic_substance = items[18]
        rate_good = int(items[19])
        rate_normal = int(items[20])
        rate_bad = int(items[21])
        image_url = items[22]

        # あー悲惨
        food = Foods(
            food_id=food_id,
            name=name,
            name_english=name_english,
            category=category,
            price=price,
            energy=energy,
            protein=protein,
            fat=fat,
            carbohydrates=carbohydrates,
            salt=salt,
            calcium=calcium,
            vegetable=vegetable,
            iron=iron,
            vitamin_a=vitamin_a,
            vitamin_b1=vitamin_b1,
            vitamin_b2=vitamin_b2,
            vitamin_c=vitamin_c,
            place_of_origin=place_of_origin,
            allergic_substance=allergic_substance,
            rate_good=rate_good,
            rate_normal=rate_normal,
            rate_bad=rate_bad,
            image_url=image_url,
        )

        food_in_table = session.query(Foods).filter(Foods.food_id == food_id).first()

        # もしテーブルになかったら追加、あったら無視
        if not food_in_table:
            print(f"Adding food_id {food_id}...")
            session.add(food)
            session.commit()
        else:
            print(f"Skipping food_id {food_id}...")

# ダミーデータの追加
# もしテーブルになかったら追加、あったら更新
# users
print("\n=== users ===")
user = Users(user_id=1, name="tarou_tanaka", email="tarou@example.com")

user_in_table = session.query(Users).filter(Users.user_id == user.user_id).first()
if not user_in_table:
    print(f"Adding user_id {user.user_id}...")
    session.add(user)
else:
    print(f"Updating user_id {user.user_id}...")
    user_in_table.name = user.name
    user_in_table.email = user.email

session.commit()

# meals
print("\n=== meals ===")

date_list = [
    datetime(2024, 9, 9, 11, 15),
    datetime(2024, 9, 10, 13, 00),
    datetime(2024, 9, 11, 12, 30),
    datetime(2024, 9, 11, 18, 00),
    datetime(2024, 9, 12, 11, 30),
]

for i in range(5):
    meal = Meals(meal_id=i + 1, user_id=1, date=date_list[i])
    meal_in_table = session.query(Meals).filter(Meals.meal_id == meal.meal_id).first()

    if not meal_in_table:
        print(f"Adding meal_id {meal.meal_id}...")
        session.add(meal)
    else:
        print(f"Updating meal_id {meal.meal_id}...")
        meal_in_table.user_id = meal.user_id
        meal_in_table.date = meal.date

session.commit()

# meal_details
print("\n=== meal_details ===")

food_id_list = [
    # ササミチーズタルタルソース, 温泉玉子, 味噌汁, ライス (中)
    [814012, 814456, 814666, 814702],
    # 春巻き, ねぎだくもやしナムル, 味噌汁, ライス (大)
    [814408, 814411, 814666, 814701],
    # 冷やし鶏天タルタルうどん, 夏のさっぱり豚汁
    [819512, 814468],
    # チキン甘辛ステーキ, 大学芋, 味噌汁, ライス (大)
    [814279, 814817, 814666, 814701],
    # カレーライス (中), 蒸し鶏サラダ
    [819272, 814490],
]

for i in range(5):
    for food_id in food_id_list[i]:
        meal_id = i + 1

        meal_details = MealDetails(meal_id=meal_id, food_id=food_id)
        meal_details_in_table = (
            session.query(MealDetails)
            .filter(
                MealDetails.meal_id == meal_details.meal_id,
                MealDetails.food_id == meal_details.food_id,
            )
            .first()
        )

        if not meal_details_in_table:
            print(f"Adding meal_id {meal_details.meal_id}...")
            session.add(meal_details)
        else:
            print(f"Updating meal_id {meal_details.meal_id}...")
            meal_details_in_table.meal_id = meal_details.meal_id
            meal_details_in_table.food_id = meal_details.food_id

session.commit()

session.close()
