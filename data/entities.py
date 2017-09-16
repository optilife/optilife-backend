from . import db


class FoodLog(db.Model):
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


class User(db.Model):
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

    def serialize(self):
        return {
            'id': self.id,
            'username': self.name,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'gender': self.gender
        }
