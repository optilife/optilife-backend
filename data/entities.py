from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


def setup():
    engine = db.create_engine('mysql+pymysql://root:@localhost')
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
