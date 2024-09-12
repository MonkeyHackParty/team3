from sqlalchemy import Column, Integer, Float, String, DateTime, BLOB
from config import base, engine

def create_table():
    base.metadata.create_all(bind=engine)

class Users(base):
    __tablename__ = 'users'

    user_id = Column('user_id', Integer, primary_key=True)
    name = Column('name', String(128))
    email = Column('email', String(128))
    password = Column('password', String(128))

class Meals(base):
    __tablename__ = "meals"

    meal_id = Column("meal_id", Integer, primary_key=True)
    user_id = Column("user_id", Integer)
    date = Column("date", DateTime)

class MealDetails(base):
    __tablename__ = "meal_details"

    meal_id = Column("meal_id", Integer, primary_key=True)
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
    image = Column("image", BLOB)
