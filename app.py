import os

from data import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from core import get_food_log
from data.entities import User, FoodLog

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()

    #insert default data
    User.insert_default_users()
    FoodLog.insert_default_foodlogs()


@app.route("/")
def hi():
    return 'hi'


if __name__ == '__main__':
    manager.run()