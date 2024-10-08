import math
import random
import sqlite3

from app.models import Foods
from app.services import get_all_food, get_food_by_id, get_history_by_user_id
from config import session


def recommend_menu(input_price, input_size, input_dessert):

    def get_all_foods_as_array():
        """
        SQLiteデータベースから全ての食品データを取得し、配列に格納する関数
        """
        foods = session.query(Foods).all()

        # データを配列（リスト）として格納する
        food_list = []

        for food in foods:
            food_data = {
                "food_id": food.food_id,
                "name": food.name,
                "category": food.category,
                "price": food.price,
                "rate_good": food.rate_good,
                "rate_normal": food.rate_normal,
                "rate_bad": food.rate_bad,
                "sum_rate": food.rate_good + food.rate_normal + food.rate_bad,
            }
            # 辞書形式でリストに追加
            food_list.append(food_data)
        return food_list

    def get_price_by_food_id(all_foods_array, target_food_id):
        """
        all_foods_array リストから target_food_id に対応する price を取得する関数
        """
        for food in all_foods_array:
            if food["food_id"] == target_food_id:
                return food["price"]
        print(print(f"Food ID {target_food_id} が見つかりませんでした。"))
        return None  # 食品IDが見つからない場合

    def get_food_details_by_id(all_foods_array, target_food_id):
        """
        all_foods_array リストから target_food_id に対応する name, category, price,sum_rate を取得して表示する関数
        """
        for food in all_foods_array:
            if food["food_id"] == target_food_id:
                print(f"food_id: {food['food_id']}", end=" ")
                print(f"Name: {food['name']}", end=" ")
                print(f"Category: {food['category']}", end=" ")
                print(f"Price: {food['price']}", end=" ")
                print(f"sum_rate: {food['sum_rate']}")
                return  # 見つかった場合、他のアイテムを探す必要はないので、関数を終了します
        # 食品IDが見つからない場合のメッセージ
        print(f"Food ID {target_food_id} not found.(get_food_details_by_id)")

    def get_i_rice(all_foods_array, i):
        """
        「rice」カテゴリーのライスをサイズで昇順にソートし、i番目に小さいライスを選択する関数
        """
        # 「rice」カテゴリーのライスをフィルタリング
        rice_list = [
            food for food in all_foods_array if food["category"] == "rice"]

        # サイズ（価格）でソート
        sorted_rice_list = sorted(rice_list, key=lambda x: x["price"])

        # i番目に小さいライスを取得
        if len(sorted_rice_list) >= i:
            i_smallest_rice = sorted_rice_list[i - 1]
            return i_smallest_rice["food_id"]
        else:
            print(i, "番目に小さいライスが見つかりません。")
            return None

    def select_sub_dish(
        all_foods_array, deside_food_data, sum_money, serect_food_num, input_price
    ):
        """
        副菜の選択を行い、合計金額と選択メニュー数を更新する関数
        """
        sub_dish_num = 0

        # 副菜の個数を数える
        for i in range(len(all_foods_array)):
            if (
                all_foods_array[i]["category"] == "sub_dish"
                and input_price >= sum_money + all_foods_array[i]["price"]
                and all_foods_array[i]["food_id"] not in deside_food_data
            ):
                if all_foods_array[i]["sum_rate"] >= 50:
                    sub_dish_num += 1
                sub_dish_num += 1

        print("sub_dish_num:", sub_dish_num)

        if sub_dish_num > 0:  # 副菜の選択
            j = 0
            sub_dish_list = [0] * sub_dish_num
            for i in range(len(all_foods_array)):
                if (
                    all_foods_array[i]["category"] == "sub_dish"
                    and input_price >= sum_money + all_foods_array[i]["price"]
                    and all_foods_array[i]["food_id"] not in deside_food_data
                ):
                    if all_foods_array[i]["sum_rate"] >= 50:
                        sub_dish_list[j] = all_foods_array[i]["food_id"]
                        j += 1
                    sub_dish_list[j] = all_foods_array[i]["food_id"]
                    j += 1

            # 副菜の選択
            deside_food_data[serect_food_num] = sub_dish_list[
                random.randint(0, len(sub_dish_list) - 1)
            ]

            # 価格の取得
            sub_dish_price = get_price_by_food_id(
                all_foods_array, deside_food_data[serect_food_num]
            )

            if sub_dish_price is not None:
                sum_money += sub_dish_price
                print("合計金額：", sum_money)
                serect_food_num += 1

                get_food_details_by_id(
                    all_foods_array, deside_food_data[serect_food_num - 1]
                )
                print("選択メニュー数：", serect_food_num)
            else:
                print(
                    f"Food ID {deside_food_data[serect_food_num]} の価格が見つかりませんでした。(select_sub_dish)"
                )

        return deside_food_data, sum_money, serect_food_num, sub_dish_num

    def update_category_bowl_prices(all_foods_array, multiplier):
        """
        all_foods_array リスト内で category が "bowl" の食品の price を任意倍し、
        1の位を0か5に切り上げて price を更新する関数
        """

        def round_price_to_nearest_5_or_0(price):
            """
            価格を5または0に切り上げる内部関数
            """
            return int(((price + 4) // 5) * 5)

        for food in all_foods_array:
            # カテゴリーが "bowl" の場合のみ価格を更新
            if food["category"] == "bowl":
                # Priceを任意倍して切り上げ処理
                new_price = food["price"] * multiplier
                rounded_price = round_price_to_nearest_5_or_0(new_price)

                # Priceを更新
                food["price"] = rounded_price
                print(
                    f"名前: {food['name']} の新しい価格: {rounded_price}(update_category_bowl_prices)"
                )

    def get_foods_by_ids(food_ids):
        """
        SQLiteデータベースから指定されたfood_idの食品データを取得し、配列に格納する関数
        :param food_ids: 取得したい食品IDのリスト
        :return: 食品データのリスト
        """
        # 指定されたfood_idの食品データを取得
        foods = session.query(Foods).filter(Foods.food_id.in_(food_ids)).all()

        # データを配列（リスト）として格納する
        food_list = []

        for food in foods:
            food_data = {
                "food_id": food.food_id,
                "name": food.name,
                "category": food.category,
                "price": food.price,
                "energy": food.energy,
                "protein": food.protein,
                "fat": food.fat,
                "carbohydrates": food.carbohydrates,
                "salt": food.salt,
                "calcium": food.calcium,
                "vegetable": food.vegetable,
                "iron": food.iron,
                "vitamin_a": food.vitamin_a,
                "vitamin_b1": food.vitamin_b1,
                "vitamin_b2": food.vitamin_b2,
                "vitamin_c": food.vitamin_c,
                "place_of_origin": food.place_of_origin,
                "allergic_substance": food.allergic_substance,
                "rate_good": food.rate_good,
                "rate_normal": food.rate_normal,
                "rate_bad": food.rate_bad,
                "sum_rate": food.rate_good + food.rate_normal + food.rate_bad,
                "image_url": food.image_url,
            }
            # 辞書形式でリストに追加
            food_list.append(food_data)

        return food_list

    def get_food_totals(serect_food_list):

        total_data = {
            "total_price": 0,
            "total_energy": 0,
            "total_protein": 0,
            "total_fat": 0,
            "total_carbohydrates": 0,
            "total_salt": 0,
            "total_calcium": 0,
            "total_vegetable": 0,
            "total_iron": 0,
            "total_vitamin_a": 0,
            "total_vitamin_b1": 0,
            "total_vitamin_b2": 0,
            "total_vitamin_c": 0,
            "total_rate_good": 0,
            "total_rate_normal": 0,
            "total_rate_bad": 0,
        }

        for food in serect_food_list:
            total_data["total_price"] += food["price"]
            total_data["total_energy"] += food["energy"]
            total_data["total_protein"] += food["protein"]
            total_data["total_fat"] += food["fat"]
            total_data["total_carbohydrates"] += food["carbohydrates"]
            total_data["total_salt"] += food["salt"]
            total_data["total_calcium"] += food["calcium"]
            total_data["total_vegetable"] += food["vegetable"]
            total_data["total_iron"] += food["iron"]
            total_data["total_vitamin_a"] += food["vitamin_a"]
            total_data["total_vitamin_b1"] += food["vitamin_b1"]
            total_data["total_vitamin_b2"] += food["vitamin_b2"]
            total_data["total_vitamin_c"] += food["vitamin_c"]
            total_data["total_rate_good"] += food["rate_good"]
            total_data["total_rate_normal"] += food["rate_normal"]
            total_data["total_rate_bad"] += food["rate_bad"]

        return total_data

    # 引数の宣言（ここでは値は変更しない。初期宣言除く）
    # input_price = 0  # 質問（値段:550,650,750）
    # input_size = 0  # 量(0=小,1=中,2=大)
    # input_dessert = True  # デザートの有無(Ture = あり, false = なし)
    j = 0  # forとかを回すようの変数
    deside_food_data = [-1] * 20  # 何を食べるか、food_idを格納
    dessert_num = 0  # デザートの総数
    main_dish_num = 0  # メインディッシュ（主菜・麺・丼/カレー）カテゴリーの総数
    sub_dish_num = 0  # 副菜カテゴリーの総数
    serect_food_num = 0  # 現在選んだメニューの数
    all_foods_array = get_all_foods_as_array()
    main_dish = "none"
    sum_money = 0
    user_id = 0
    recent_main_dish_num = 0
    recent_bowl_num = 0
    recent_noodle_num = 0

    # 変数の代入（仮）
    # 質問
    # input_price = 550
    # input_size = 1  # (0=小,1=中,2=大)
    # input_dessert = True

    # デザートが最高額の時のみ選択できるようにする
    if input_price != 750:
        input_dessert = False

    # デザートを追加
    if input_dessert == True:
        # デザートの個数を調べる
        for i in range(len(all_foods_array)):
            if all_foods_array[i]["category"] == "dessert":
                if all_foods_array[i]["sum_rate"] >= 50:
                    dessert_num += 1
                dessert_num += 1
        print("dessert_num:", dessert_num)

        # デザート追加処理
        if dessert_num > 0:
            j = 0
            dessert_list = [0] * dessert_num
            for i in range(len(all_foods_array)):
                if all_foods_array[i]["category"] == "dessert":
                    if all_foods_array[i]["sum_rate"] >= 50:
                        dessert_list[j] = all_foods_array[i]["food_id"]
                        j += 1
                    dessert_list[j] = all_foods_array[i]["food_id"]
                    j += 1

            deside_food_data[serect_food_num] = dessert_list[
                random.randint(0, len(dessert_list) - 1)
            ]
            sum_money += get_price_by_food_id(
                all_foods_array, deside_food_data[serect_food_num]
            )
            print("合計金額：", sum_money)
            serect_food_num += 1

        get_food_details_by_id(
            all_foods_array, deside_food_data[serect_food_num - 1])
        print("選択メニュー数：", serect_food_num)

    # 記録（仮）
    '''
    food_item = {
        "category": "main_dish",
        "name": "ライス",
        "name_english": "Boiled rice",
        "price": 126,
        "energy": 374,
        "protein": 6.0,
        "fat": 0.7,
        "carbohydrates": 89.0,
        "salt": 0.0,
        "calcium": 7,
        "vegetable": 0,
        "iron": 0.2,
        "vitamin_a": 0,
        "vitamin_b1": 0.05,
        "vitamin_b2": 0.02,
        "vitamin_c": 0,
        "place_of_origin": "米（国産）",
        "allergic_substance": "",
        "rate_good": 9,
        "rate_normal": 1,
        "rate_bad": 3,
        "image_url": "画像ファイルのURL",
    }

    recent_list = [{"date": "2024-09-10", "meal_id": 1, "foods": [food_item]}]
    '''
    # 主食の選択（主菜・麺・丼/カレー）＋記録参照
    # (本番では下のコメントアウトを消し、上"記録（仮）"を消すこと)
    recent_list = get_history_by_user_id(user_id, True)

    if recent_list is not None and len(recent_list) > 0:
        for i in recent_list:
            for j in i["foods"]:
                if j["category"] == "main_dish":
                    recent_main_dish_num += 1
                elif j["category"] == "bowl":
                    recent_bowl_num += 1
                elif j["category"] == "noodle":
                    recent_noodle_num += 1

    print(
        "main:",
        recent_main_dish_num,
        "bowl:",
        recent_bowl_num,
        "noodle:",
        recent_noodle_num,
    )

    main_dish = random.randint(0, 4)
    if main_dish == 0:
        main_dish = "main_dish"
    elif main_dish == 1:
        main_dish = "bowl"
    elif main_dish == 2:
        main_dish = "noodle"
    else:
        min_value = min(recent_main_dish_num,
                        recent_bowl_num, recent_noodle_num)
        if min_value == recent_main_dish_num:
            main_dish = "main_dish"
        elif min_value == recent_bowl_num:
            main_dish = "bowl"
        else:
            main_dish = "noodle"
    print(main_dish)

    # ライスの選択（主菜のときのみ）
    if main_dish == "main_dish":
        if input_size == 0:
            i = 2
        elif input_size == 1:
            i = 3
        else:
            i = 4

        deside_food_data[serect_food_num] = get_i_rice(all_foods_array, i)
        sum_money += get_price_by_food_id(
            all_foods_array, deside_food_data[serect_food_num]
        )
        print("合計金額：", sum_money)
        serect_food_num += 1

        get_food_details_by_id(
            all_foods_array, deside_food_data[serect_food_num - 1])
        print("選択メニュー数：", serect_food_num)

    # ここでサイズを大小させる(丼/カレー全てに適応)

    if input_size == 2:
        update_category_bowl_prices(all_foods_array, 1.147)
    elif input_size == 0:
        update_category_bowl_prices(all_foods_array, 0.88888888)

    # 選択した主食カテゴリーの個数を調べる
    for i in range(len(all_foods_array)):
        if (
            all_foods_array[i]["category"] == main_dish
            and input_price >= sum_money + all_foods_array[i]["price"]
        ):
            if all_foods_array[i]["sum_rate"] >= 50:
                main_dish_num += 1
            main_dish_num += 1

    print("main_dish_num:", main_dish_num)

    # メインディッシュの選択
    if main_dish_num > 0:
        j = 0
        main_dish_list = [0] * main_dish_num
        for i in range(len(all_foods_array)):
            if (
                all_foods_array[i]["category"] == main_dish
                and input_price >= sum_money + all_foods_array[i]["price"]
            ):
                if all_foods_array[i]["sum_rate"] >= 50:
                    main_dish_list[j] = all_foods_array[i]["food_id"]
                    j += 1
                main_dish_list[j] = all_foods_array[i]["food_id"]
                j += 1

        deside_food_data[serect_food_num] = main_dish_list[
            random.randint(0, len(main_dish_list) - 1)
        ]

        sum_money += get_price_by_food_id(
            all_foods_array, deside_food_data[serect_food_num]
        )

        print("合計金額：", sum_money)
        serect_food_num += 1

        get_food_details_by_id(
            all_foods_array, deside_food_data[serect_food_num - 1])
        print("選択メニュー数：", serect_food_num)

    # 副菜の決定（お金が無くなるまで）
    while input_price >= sum_money:
        deside_food_data, sum_money, serect_food_num, sub_dish_num = select_sub_dish(
            all_foods_array, deside_food_data, sum_money, serect_food_num, input_price
        )
        if sub_dish_num == 0:
            break

    print(sum_money)
    print(deside_food_data)
    deside_food_id = [0] * serect_food_num
    for i in range(serect_food_num):
        deside_food_id[i] = deside_food_data[i]

    print(deside_food_id)

    serect_food_list = get_foods_by_ids(deside_food_id)
    print(serect_food_list)  # 渡すもの１（個別データ）
    toatal_food_data = get_food_totals(serect_food_list)
    print(toatal_food_data)  # 渡すもの２（合計データ）

    # 詳細データをリストで表示v
    return serect_food_list, toatal_food_data


''''''
if __name__ == "__main__":
    #  例

    list = recommend_menu(550, 2, True)  # listはfood_idを格納しているリスト
    print(list)
