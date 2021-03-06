import os
import random
from datetime import datetime, timedelta

from data import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from data.entities import User, FoodLog
from flask_restful import Resource, Api, reqparse
from flask import jsonify
from core import get_food_labels, get_food_health_value, get_health_index, save_food_log_entry, get_daily_calories, \
    get_daily_goal, get_daily_calories_percentage
import base64
from sqlalchemy.sql import func

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

api = Api(app)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()

    #insert default data
    User.insert_default_users()
    FoodLog.insert_default_foodlogs()


userParser = reqparse.RequestParser()
userParser.add_argument('id')
userParser.add_argument('username')
userParser.add_argument('mail')
userParser.add_argument('password')
userParser.add_argument('age')
userParser.add_argument('height')
userParser.add_argument('weight')
userParser.add_argument('gender')
userParser.add_argument('vegeterian')


class UserHandler(Resource):
    def get(self, user_id):
        return User.query.filter_by(id=user_id).first().serialize()

    def put(self, user_id):
        args = userParser.parse_args()
        usr = User.query.filter_by(id=user_id).first()
        usr.username = args['username']
        usr.mail = args['mail']
        usr.password_hash = args['password']
        usr.age = args['age']
        usr.height = args['height']
        usr.weight = args['weight']
        usr.gender = args['gender']
        usr.vegeterian = args['vegeterian']
        db.session.add(usr)
        db.session.commit()
        return True


api.add_resource(UserHandler, '/api/users/<int:user_id>')

userLoginParser = reqparse.RequestParser()
userLoginParser.add_argument('username')
userLoginParser.add_argument('password')


class UserLoginHandler(Resource):
    def post(self):
        args = userLoginParser.parse_args()
        username = args['username']
        password_hash = args['password']
        usr = User.query.filter_by(username=username, password_hash=password_hash).first()
        if usr != None:
            return usr.id
        else:
            return False


api.add_resource(UserLoginHandler, '/api/users/login')

foodParser = reqparse.RequestParser()
foodParser.add_argument("image")


class HealthIndexHandler(Resource):
    def get(self, user_id):
        print(get_daily_calories(user_id))
        return jsonify(self.serialize(user_id))

    def serialize(self, user_id):
        if get_daily_calories(user_id) is not None:
            calories = float(get_daily_calories(user_id))
            calories_percentage = float(get_daily_calories_percentage(user_id))
        else:
            calories = 0.0
            calories_percentage = 0.0
        return {
            'health-index': 100 - get_health_index(user_id) if not None else 0.0,
            'calories_today': calories,
            'calories_today_percentage': calories_percentage,
            'challenges_won': random.randint(20,100) if not None else 0.0,
            'daily_goal': get_daily_goal(user_id) if not None else 0.0
        }


api.add_resource(HealthIndexHandler, '/api/users/health-index/<int:user_id>')


class FoodHandler(Resource):
    def post(self):
        args = foodParser.parse_args()
        encoded_image = base64.b64decode(args['image'])
        return get_food_labels(encoded_image)


api.add_resource(FoodHandler, '/api/food/')


class FoodLabelHandler(Resource):
    def get(self, label):
        return get_food_health_value(label)


api.add_resource(FoodLabelHandler, '/api/food/<string:label>')


foodLogParser = reqparse.RequestParser()
foodLogParser.add_argument("label")


class FoodLogHandler(Resource):
    def get(self, user_id):
        previous = FoodLog.query.filter(FoodLog.user_id == user_id,
                                        FoodLog.timestamp >= datetime.now() - timedelta(days=60),
                                       FoodLog.timestamp <= datetime.now() - timedelta(days=30)).all()
        current = FoodLog.query.filter(FoodLog.user_id == user_id,
                                       FoodLog.timestamp >= datetime.now() - timedelta(days=30),
                                        FoodLog.timestamp <= datetime.now()).all()
        return jsonify(self.serialize_log(previous, current))

    def post(self, user_id):
        args = foodLogParser.parse_args()
        label = args["label"]
        health_value = get_food_health_value(label)
        return save_food_log_entry(name=label, health_value=health_value, user_id=user_id)

    def serialize_log(self, previous, current):
        data = {'previous': [f.serialize() for f in previous], 'current': [f.serialize() for f in current]}
        return data



api.add_resource(FoodLogHandler, '/api/food/log/<int:user_id>')


if __name__ == '__main__':
    manager.run()