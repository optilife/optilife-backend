from Vision.Helper import get_labels_from_image, nutritionix_wrapper
from data import db
from data.entities import User, FoodLog

# hard coded user
user = db.session.query(User).one()


def get_food_labels(img_path):
    return get_labels_from_image(img_path)


def get_food_health_value(label):
    return nutritionix_wrapper(label)


# def save_food_log_entry(user, name, health_value):
def save_food_log_entry(name, health_value):
    food = FoodLog(name=name, health_value=health_value)
    db.session.add(food)
    db.session.commit()


# def get_food_log(user):
def get_food_log():
    return FoodLog.query.filter_by(user=user)

