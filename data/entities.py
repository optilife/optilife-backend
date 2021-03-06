import datetime
import os
import random

from sqlalchemy.ext.hybrid import hybrid_property

from . import db


dir_path = os.path.dirname(os.path.realpath(__file__))


def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False


def random_price():
    return round(random.uniform(0.5, 6.5) * 20) / 20


def random_calories():
    return random.randint(40, 270)


def random_date():
    year = 2017
    month = random.choice(range(8,10))
    day = random.choice(range(1,31))
    return datetime.datetime(year, month, day).date()

class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)


class FoodLog(CRUDMixin, db.Model):
    __tablename__ = "foodlogs"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    health_value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.Date, default=datetime.datetime.now().date)
    price = db.Column(db.Float, default=random_price)
    calories = db.Column(db.Integer, default=random_calories)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<FoodLog %r>' % self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'health_value': self.health_value,
            'user_id': self.user_id,
            'timestamp': self.timestamp
        }


    @staticmethod
    def insert_default_foodlogs():
        with open(os.path.join(dir_path, 'default_data/foodlog'), 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                name, health_value, user_id = line.split(',')
                FoodLog.create(
                    name=name,
                    health_value=health_value,
                    user_id=user_id
                )


class User(CRUDMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String(128), unique=True, index=True, nullable=False)
    mail = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    vegetarian = db.Column(db.Boolean, default=False,)
    monthly_budget = db.Column(db.Float, nullable=False)
    foodlogs = db.relationship('FoodLog', backref='role')

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = password

    @hybrid_property
    def actual_budget(self):
        costs = 0
        for foodlog in self.foodlogs:
            costs = costs + foodlog.price
        return self.monthly_budget - costs

    @staticmethod
    def insert_default_users():
        with open(os.path.join(dir_path, 'default_data/user'), 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                name, email, password, age, height, weight, gender, vegetarian, monthly_budget = line.split(',')
                User.create(
                    username=name,
                    mail=email,
                    password=password,
                    age=age,
                    height=height,
                    weight=weight,
                    gender=gender,
                    vegetarian=str_to_bool(vegetarian),
                    monthly_budget= monthly_budget
                    )


    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'mail': self.mail,
            'password_hash': self.password_hash,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'gender': self.gender,
            'vegeterian': self.vegetarian,
            'monthly_budget': self.monthly_budget,
            'actual_budget': self.actual_budget
        }
