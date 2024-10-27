# app/routes.py
from flask import render_template, redirect, url_for, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, FoodLog, FitnessLog
from . import db
from functools import wraps
from datetime import datetime

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_routes(app):
    @app.route('/')
    @login_required
    def home():
        return render_template('dashboard.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/goals')
    @login_required
    def goals():
        user = User.query.filter_by(username=session['username']).first()
        if not user:
            return redirect(url_for('login'))
        return render_template('goals.html', user=user)

    @app.route('/foods')
    @login_required
    def food():
        return render_template('foods.html')

    @app.route('/activities')
    @login_required
    def activities():
        return render_template('activities.html')

    @app.route('/summary')
    @login_required
    def summary():
        return render_template('summary.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.form
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'error': 'Username and password are required'}), 400

            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['username'] = username
                return jsonify({'message': 'Successful login'}), 200
            else:
                return jsonify({'error': 'Invalid username or password'}), 401

        return render_template('login.html')

    @app.route('/register', methods=['POST'])
    def register():
        data = request.form
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'User already exists!'}), 400

        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully!'}), 201

    @app.route('/logout', methods=['POST'])
    def logout():
        session.pop('username', None)
        return jsonify({'message': 'Logged out successfully'}), 200

    @app.route('/api/update-goal', methods=['POST'])
    @login_required
    def update_goal():
        data = request.get_json()
        user = User.query.filter_by(username=session['username']).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user.calorie_goal = data.get('calorie_goal', user.calorie_goal)
        user.protein_goal = data.get('protein_goal', user.protein_goal)
        user.fat_goal = data.get('fat_goal', user.fat_goal)
        user.carbs_goal = data.get('carbs_goal', user.carbs_goal)
        db.session.commit()
        
        return jsonify({'message': 'Goals updated successfully!'}), 200

    @app.route('/api/food', methods=['POST'])
    @login_required
    def add_food():
        data = request.get_json()
        user = User.query.filter_by(username=session['username']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if not data.get('food') or data.get('calories') is None or data.get('protein') is None \
           or data.get('fat') is None or data.get('carbs') is None:
            return jsonify({'error': 'Food name, calories, protein, fat, and carbs are required'}), 400

        selected_date = data.get('date', datetime.today().strftime('%Y-%m-%d'))
        new_food_log = FoodLog(
            user_id=user.id,
            date=selected_date,
            food=data.get('food'),
            calories=data.get('calories'),
            protein=data.get('protein'),
            fat=data.get('fat'),
            carbs=data.get('carbs')
        )
        db.session.add(new_food_log)
        db.session.commit()
        
        return jsonify({'message': 'Food added successfully!'}), 201

    @app.route('/api/food', methods=['DELETE'])
    @login_required
    def delete_food():
        data = request.get_json()
        food_id = data.get('food_id')

        if food_id is None:
            return jsonify({'error': 'Food ID is required'}), 400

        food_log = FoodLog.query.get(food_id)
        if food_log and food_log.user.username == session['username']:
            db.session.delete(food_log)
            db.session.commit()
            return jsonify({'message': 'Food deleted successfully!'}), 200

        return jsonify({'error': 'Food item not found!'}), 404

    @app.route('/api/fitness', methods=['POST'])
    @login_required
    def add_fitness():
        data = request.get_json()
        user = User.query.filter_by(username=session['username']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if not data.get('exercise') or data.get('kcal_burned') is None:
            return jsonify({'error': 'Exercise and kcal burned are required'}), 400

        selected_date = data.get('date', datetime.today().strftime('%Y-%m-%d'))
        new_fitness_log = FitnessLog(
            user_id=user.id,
            date=selected_date,
            exercise=data.get('exercise'),
            kcal_burned=data.get('kcal_burned')
        )
        db.session.add(new_fitness_log)
        db.session.commit()

        return jsonify({'message': 'Exercise added successfully!'}), 201

    @app.route('/api/fitness', methods=['DELETE'])
    @login_required
    def delete_fitness():
        data = request.get_json()
        fitness_id = data.get('fitness_id')

        if fitness_id is None:
            return jsonify({'error': 'Fitness ID is required'}), 400

        fitness_log = FitnessLog.query.get(fitness_id)
        if fitness_log and fitness_log.user.username == session['username']:
            db.session.delete(fitness_log)
            db.session.commit()
            return jsonify({'message': 'Exercise deleted successfully!'}), 200

        return jsonify({'error': 'Exercise not found!'}), 404

    @app.route('/daily-summary', methods=['GET'])
    @login_required
    def daily_summary():
        user = User.query.filter_by(username=session['username']).first()
        date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))

        if not user:
            return jsonify({'error': 'User not found'}), 404

        food_log = FoodLog.query.filter_by(user_id=user.id, date=date).all()
        fitness_log = FitnessLog.query.filter_by(user_id=user.id, date=date).all()

        total_calories_consumed = sum(item.calories for item in food_log)
        total_calories_burned = sum(item.kcal_burned for item in fitness_log)
        total_protein = sum(item.protein for item in food_log)
        total_fat = sum(item.fat for item in food_log)
        total_carbs = sum(item.carbs for item in food_log)

        return jsonify({
            'calories_goal': user.calorie_goal,
            'protein_goal': user.protein_goal,
            'fat_goal': user.fat_goal,
            'carbs_goal': user.carbs_goal,
            'total_calories_consumed': total_calories_consumed,
            'total_calories_burned': total_calories_burned,
            'net_calories': total_calories_consumed - total_calories_burned,
            'total_protein': total_protein,
            'total_fat': total_fat,
            'total_carbs': total_carbs,
            'food_log': [{'id': item.id, 'food': item.food, 'calories': item.calories, 'protein': item.protein, 'fat': item.fat, 'carbs': item.carbs} for item in food_log],
            'fitness_log': [{'id': item.id, 'exercise': item.exercise, 'kcal_burned': item.kcal_burned} for item in fitness_log]
        })