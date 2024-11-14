# app/models.py
from . import db, ma
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# FoodLog model
class FoodLog(db.Model):
    __tablename__ = 'food_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    food = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    carbs = db.Column(db.Integer)

# FitnessLog model
class FitnessLog(db.Model):
    __tablename__ = 'fitness_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    exercise = db.Column(db.String(100))
    kcal_burned = db.Column(db.Integer)

# User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    calorie_goal = db.Column(db.Integer, default=2000)
    protein_goal = db.Column(db.Integer, default=150)
    fat_goal = db.Column(db.Integer, default=70)
    carbs_goal = db.Column(db.Integer, default=250)
    food_logs = db.relationship('FoodLog', backref='user', lazy=True)
    fitness_logs = db.relationship('FitnessLog', backref='user', lazy=True)

# User Schema
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

# FoodLog Schema
class FoodLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FoodLog
        include_fk = True
        load_instance = True
    # user = fields.Nested('UserSchema', exclude=('food_logs', 'fitness_logs'))

# FitnessLog Schema
class FitnessLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FitnessLog
        include_fk = True
        load_instance = True
    # user = fields.Nested('UserSchema', exclude=('food_logs', 'fitness_logs'))