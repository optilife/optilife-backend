from datetime import datetime

from sqlalchemy.sql import func

from Vision.Helper import get_labels_from_image, nutritionix_wrapper
from data import db
from data.entities import User, FoodLog
from flask import jsonify


def get_food_labels(image):
    labels = get_labels_from_image(image)
    return jsonify(foodlabels=[l.description for l in labels])


def get_food_health_value(label):
    return nutritionix_wrapper(label)


def save_food_log_entry(user_id, name, health_value):
    food = FoodLog(name=name, health_value=health_value, user_id=user_id)
    db.session.add(food)
    db.session.commit()
    return food.id


def get_food_log(user):
    result = FoodLog.query.filter_by(user_id=user.id).all()
    return jsonify(food_log=[r.serialize() for r in result])


def get_health_index(user):
    health_index = db.session.query(func.avg(FoodLog.health_value)).filter(FoodLog.user_id == user).first()
    return round(health_index[0] * 10, 1)


def get_daily_calories(user):
    calorie_sum = db.session.query(func.sum(FoodLog.calories)).filter(FoodLog.user_id == user,
                                                               FoodLog.timestamp == datetime.now().date()).first()[0]
    if calorie_sum is None:
        calorie_sum = 0

    ratio = calorie_sum / 2000
    return min(ratio, 1) * 100

def get_daily_goal(user):
    cnt = db.session.query(func.count(FoodLog.user_id)).filter(FoodLog.user_id == user,
                                                               FoodLog.timestamp == datetime.now().date()).first()[0]
    if cnt == 0:
        return 0
    elif cnt == 1:
        return 33
    elif cnt == 2:
        return 66
    else:
        return 100


def get_last_month_food(user):
    print(db.session.query)



