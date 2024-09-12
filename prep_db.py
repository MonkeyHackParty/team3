from config import session
import app.models
from app.models import Users, Meals, MealDetails, Foods

# テーブルの作成
app.models.create_table()

# foodsテーブルにfoods.csvからのデータをいれる
is_first_line = True
with open('foods.csv', mode='r') as f:
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

        print(f"Adding food_id {food_id}...")

        # あー悲惨
        food = Foods(food_id=food_id, name=name, name_english=name_english, category=category, price=price, energy=energy, protein=protein, fat=fat, carbohydrates=carbohydrates, salt=salt, calcium=calcium, vegetable=vegetable, iron=iron, vitamin_a=vitamin_a, vitamin_b1=vitamin_b1, vitamin_b2=vitamin_b2, vitamin_c=vitamin_c, place_of_origin=place_of_origin, allergic_substance=allergic_substance, rate_good=rate_good, rate_normal=rate_normal, rate_bad=rate_bad, image_url=image_url)

        # TODO conflictしたら値を更新する
        try:
            session.add(food)
            session.commit()
        except Exception as e:
            print("Failed to add to database!")
            print(e)

session.close()
