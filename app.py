import os

from data import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from data.entities import User, FoodLog
from flask_restful import Resource, Api

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


class UserHandler(Resource):
    def get(self, user_id):
        return User.query.filter_by(id=user_id).first().serialize()


api.add_resource(UserHandler, '/api/users/<int:user_id>')


if __name__ == '__main__':
    manager.run()