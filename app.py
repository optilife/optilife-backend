import os

from data import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from data.entities import User, FoodLog
from flask_restful import Resource, Api, reqparse
from flask import jsonify
from core import get_food_labels, get_food_health_value
import base64

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
foodLogParser.add_argument("name")
foodLogParser.add_argument("health_value")

class FoodLogHandler(Resource):
    def get(self, user_id):
        log = FoodLog.query.filter_by(user_id=user_id).all()
        return jsonify(food_log=[f.serialize() for f in log])

    def post(self, user_id):
        args = foodLogParser.parse_args()
        log_entry = FoodLog(name=args['name'], health_value=args['health_value'], user_id=user_id)
        db.session.add(log_entry)
        db.session.commit()
        return log_entry.id


api.add_resource(FoodLogHandler, '/api/food/log/<int:user_id>')


if __name__ == '__main__':
    manager.run()