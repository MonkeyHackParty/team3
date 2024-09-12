import requests
from bs4 import BeautifulSoup

def sanitize_element(s):
    for i in ["円", "kcal", "mg", "μg", "g"]:
        s = s.replace(i, "")
    return s

def scrape_by_food_id(food_id, category):
    category = category_to_string(category)

    url = f"{BASE_URL}/detail.php?t={PLACE}&c={food_id}"

    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser")

    name_mixed = soup.select("div#main h1")[0].text
    name_english = soup.select("div#main h1 span")[0].text
    name = name_mixed.replace(name_english, "")
    # print(name)
    # print(name_english)

    is_price = True
    elements = ""
    values = soup.select("ul.detail > li")
    for v in values:
        try:
            element = v.find("span", class_="price").text
            element = sanitize_element(element)

            # もし0番目(価格)で大中小の3つの値段がある場合、中の値段だけにする
            if is_price and "中" in element:
                element = element.split(" ")[0].replace("中", "")

            elements += element + ","
            is_price = False
        except Exception as e:
            break
    # Remove the last comma of elements
    elements = elements[:-1]
    # print(elements)

    icon_list = soup.select("li.allergy ul.icon-list > li")
    allergic_substance = ""

    for icon in icon_list:
        allergy = icon["class"][0].replace("icon_", "")
        allergic_substance += allergy + " "

    # Remove the last colon
    allergic_substance = allergic_substance[:-1]
    # print(allergic_substance)

    rate_good = soup.select(".evaluation .eval1")[0].text
    rate_normal = soup.select(".evaluation .eval2")[0].text
    rate_bad = soup.select(".evaluation .eval3")[0].text
    # print(rate_good)
    # print(rate_normal)
    # print(rate_bad)

    image_url = soup.select("img.menuimg")[0]["src"]
    # print(image_url)

    csv_str = f"{name},{name_english},{category},{elements},{allergic_substance},{rate_good},{rate_normal},{rate_bad},{image_url}"

    return csv_str

def category_to_string(category):
    if category == "on_a":
        return "main_dish"
    elif category == "on_b":
        return "sub_dish"
    elif category == "on_c":
        return "noodle"
    elif category == "on_d":
        return "bowl"
    elif category == "on_e":
        return "desert"
    elif category == "on_bunrui5":
        return "rice"

# pip install requests
# pip install beautifulsoup4

# tパラメータ
# キャンパスの指定?
# 650337 -> OICキャンパス

# aパラメータ
# カテゴリの指定
# on_a -> 主菜
# on_b -> 副菜
# on_c -> 麺類
# on_d -> 丼・カレー
# on_e -> デザート
# on_bunrui5 -> ライス

# cパラメータ
# 食べ物のid

BASE_URL = "https://west2-univ.jp/sp"
PLACE = 650337

# カテゴリ別に食べ物IDをスクレイピングする
food_list = []
category_list = ["on_a", "on_b", "on_c", "on_d", "on_e", "on_bunrui5"]

print("Scraping food_id...")

# TODO 並列処理にする
for category in category_list:
    url = f"{BASE_URL}/menu_load.php?t={PLACE}&a={category}"
    # print(url)
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser")

    foods = soup.select("li")

    for food in foods:
        food_id = food.find("a")["href"].replace(f"detail.php?t={PLACE}&c=", "")
        food_list.append([food_id, category])

# print("food_id_list:", food_id_list)
print(f"Found {len(food_list)} food_id!")

csv_heading = "name,name_english,category,price,energy,protein,fat,carbohydrates,salt,calcium,vegetable,iron,vitamin_a,vitamin_b1,vitamin_b2,vitamin_c,place_of_origin,allergic_substance,rate_good,rate_normal,rate_bad,image" + "\n"
csv_str = ""

# food_id_listをもとにそれぞれの食べ物の詳細をスクレイピングする
for food in food_list:
    food_id = food[0]
    category = food[1]

    print(f"Scraping food_id {food_id}...")

    csv_str += scrape_by_food_id(food_id, category) + "\n"

with open('foods.csv', mode='w') as f:
    f.write(csv_heading)
    f.write(csv_str)

print("Wrote food data to foods.csv!")
