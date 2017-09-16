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


def save_food_log_entry(user, name, health_value):
    food = FoodLog(name=name, health_value=health_value, user_id=user.id)
    db.session.add(food)
    db.session.commit()


def get_food_log(user):
    result = FoodLog.query.filter_by(user_id=user.id).all()
    return jsonify(food_log=[r.serialize() for r in result])


def get_health_index(user):
    health_index = db.session.query(func.avg(FoodLog.health_value)).filter(FoodLog.user_id == user).first()
    return round(health_index[0] * 10, 1)



