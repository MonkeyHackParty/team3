from sqlalchemy import Column, DateTime, Float, Integer, String

from config import base, engine

# https://zenn.dev/re24_1986/articles/8520ac3f9a0187


def create_table():
    base.metadata.create_all(bind=engine)


class Users(base):
    __tablename__ = "users"

    user_id = Column("user_id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(128))
    email = Column("email", String(64))
    password = Column("password", String(64))


class Meals(base):
    __tablename__ = "meals"

    meal_id = Column("meal_id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer)
    date = Column("date", DateTime)


class MealDetails(base):
    __tablename__ = "meal_details"

    meal_detail_id = Column(
        "meal_detail_id", Integer, primary_key=True, autoincrement=True
    )
    meal_id = Column("meal_id", Integer)
    food_id = Column("food_id", Integer)


class Foods(base):
    __tablename__ = "foods"

    food_id = Column("food_id", Integer, primary_key=True)
    category = Column("category", String(64))
    name = Column("name", String(128))
    name_english = Column("name_english", String(128))
    price = Column("price", Integer)
    energy = Column("energy", Integer)
    protein = Column("protein", Float)
    fat = Column("fat", Float)
    carbohydrates = Column("carbohydrates", Float)
    salt = Column("salt", Float)
    calcium = Column("calcium", Integer)
    vegetable = Column("vegetable", Integer)
    iron = Column("iron", Float)
    vitamin_a = Column("vitamin_a", Integer)
    vitamin_b1 = Column("vitamin_b1", Float)
    vitamin_b2 = Column("vitamin_b2", Float)
    vitamin_c = Column("vitamin_c", Integer)
    place_of_origin = Column("place_of_origin", String(128))
    allergic_substance = Column("allergic_substance", String(128))
    rate_good = Column("rate_good", Integer)
    rate_normal = Column("rate_normal", Integer)
    rate_bad = Column("rate_bad", Integer)
    image_url = Column("image_url", String(128))
