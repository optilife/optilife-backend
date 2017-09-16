import os

from . import db


dir_path = os.path.dirname(os.path.realpath(__file__))


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
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    health_value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<FoodLog %r>' % self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'health_value': self.health_value,
            'user_id': self.user_id
        }


    @staticmethod
    def insert_default_foodlogs():
        with open(os.path.join(dir_path, 'default_data/foodlog'), 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                id, name, health_value, user_id = line.split(',')
                FoodLog.create(
                    id=id,
                    name=name,
                    health_value=health_value,
                    user_id=user_id
                )


class User(CRUDMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(128), unique=True, index=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    foodlogs = db.relationship('FoodLog', backref='role')

    def __repr__(self):
        return '<User %r>' % self.username


    @staticmethod
    def insert_default_users():
        with open(os.path.join(dir_path, 'default_data/user'), 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                id, name, age, height, weight, gender = line.split(',')
                User.create(
                    id=id,
                    username=name,
                    age=age,
                    height=height,
                    weight=weight,
                    gender=gender
                    )


def serialize(self):
    return {
        'id': self.id,
        'username': self.name,
        'age': self.age,
        'height': self.height,
        'weight': self.weight,
        'gender': self.gender
    }
