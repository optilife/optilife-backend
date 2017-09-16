import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(find_dotenv())

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_SERVER_URL') + \
                                        os.environ.get("DEV_DATABASE_NAME")
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


port = int(os.getenv('PORT', '3000'))

# The database classes and functions would actually belong into a separate file,
# but this leads to circular references, we cannot resolve with our Python knowledge.
# And this is a hackathon anyways...


def create_db():
    engine = db.create_engine(os.environ.get('DEV_DATABASE_SERVER_URL'))
    engine.execute("CREATE DATABASE IF NOT EXISTS optilife")
    engine.execute("USE optilife")
    db.drop_all()
    db.create_all()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(128), unique=True, index=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def hello_world():
    return


@app.route('/setup_db')
def setup_db():
    msg = "DB dropped and recreated"

    try:
        create_db()
    except Exception as ex:
        msg = ex;

    return msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)