# app/models/models.py
from .. import db, ma
from marshmallow import fields, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime

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

# User Schema
class UserSchema(SQLAlchemyAutoSchema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

    class Meta:
        model = User
        load_instance = True
        include_fk = True

    @validates('username')
    def validate_username(self, value):
        if not value:
            raise ValidationError('Username is required.')

    @validates('password')
    def validate_password(self, value):
        if not value:
            raise ValidationError('Password is required.')
        

# Goal Schema
class GoalsSchema(SQLAlchemyAutoSchema):
    calorie_goal = fields.Integer(required=True, validate=lambda n: n > 0)
    protein_goal = fields.Integer(required=True, validate=lambda n: n > 0)
    fat_goal = fields.Integer(required=True, validate=lambda n: n > 0)
    carbs_goal = fields.Integer(required=True, validate=lambda n: n > 0)
    
    class Meta:
        load_instance = False

    @validates('calorie_goal')
    def validate_calorie_goal(self, value):
        if value <= 0:
            raise ValidationError('Calorie goal must be greater than zero.')

    @validates('protein_goal')
    def validate_protein_goal(self, value):
        if value <= 0:
            raise ValidationError('Protein goal must be greater than zero.')

    @validates('fat_goal')
    def validate_fat_goal(self, value):
        if value <= 0:
            raise ValidationError('Fat goal must be greater than zero.')

    @validates('carbs_goal')
    def validate_carbs_goal(self, value):
        if value <= 0:
            raise ValidationError('Carbs goal must be greater than zero.')

# FoodLog Schema
class FoodLogSchema(SQLAlchemyAutoSchema):
    date = fields.Str(required=True)
    food = fields.Str(required=True)
    calories = fields.Integer(required=True, validate=lambda n: n >= 0)
    protein = fields.Integer(required=True, validate=lambda n: n >= 0)
    fat = fields.Integer(required=True, validate=lambda n: n >= 0)
    carbs = fields.Integer(required=True, validate=lambda n: n >= 0)

    class Meta:
        model = FoodLog
        include_fk = True
        load_instance = True

    @validates('date')
    def validate_date(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Invalid date format. Use YYYY-MM-DD.')

    @validates('calories')
    def validate_calories(self, value):
        if value is None or value < 0:
            raise ValidationError('Calories must not be negative.')

    @validates('protein')
    def validate_protein(self, value):
        if value is None or value < 0:
            raise ValidationError('Protein must not be negative.')

    @validates('fat')
    def validate_fat(self, value):
        if value is None or value < 0:
            raise ValidationError('Fat must not be negative.')

    @validates('carbs')
    def validate_carbs(self, value):
        if value is None or value < 0:
            raise ValidationError('Carbs must not be negative.')

# FitnessLog Schema
class FitnessLogSchema(SQLAlchemyAutoSchema):
    date = fields.Str(required=True)
    exercise = fields.Str(required=True)
    kcal_burned = fields.Integer(required=True, validate=lambda n: n >= 0)

    class Meta:
        model = FitnessLog
        include_fk = True
        load_instance = True

    @validates('date')
    def validate_date(self, value):
        try:
            # Ensure the date is in the correct format
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Invalid date format. Use YYYY-MM-DD.')

    @validates('exercise')
    def validate_exercise(self, value):
        if not value:
            raise ValidationError('Exercise name is required.')

    @validates('kcal_burned')
    def validate_kcal_burned(self, value):
        if value is None or value < 0:
            raise ValidationError('Calories burned must be a non-negative integer.')