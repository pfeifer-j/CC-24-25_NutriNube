# app/routes.py
from flask import render_template, redirect, url_for, request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, FoodLog, FitnessLog, UserSchema, FoodLogSchema, FitnessLogSchema
from . import db
from functools import wraps
from datetime import datetime
from marshmallow import ValidationError

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            current_app.logger.info({
                'event': 'access_denied',
                'message': 'User attempted to access a protected route without logging in',
                'route': request.path
            })
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function   

def init_routes(app):
    @app.route('/')
    @login_required
    def home():
        try:
            app.logger.info({
                'event': 'route_access',
                'route': '/',
                'username': session.get('username', 'anonymous')
            })
            return render_template('dashboard.html')
        except Exception as e:
            current_app.logger.error({
                'event': 'home_page_error',
                'message': f"An error occurred: {str(e)}"
            })
            return "An internal error occurred", 500

    @app.route('/dashboard')
    @login_required
    def dashboard():
        try:
            app.logger.info({
                'event': 'route_access',
                'route': '/dashboard',
                'username': session.get('username', 'anonymous')
            })
            return render_template('dashboard.html')
        except Exception as e:
            current_app.logger.error({
                'event': 'dashboard_page_error',
                'message': f"An error occurred: {str(e)}"
            })
            return "An internal error occurred", 500

    @app.route('/goals')
    @login_required
    def goals():
        try:
            user = User.query.filter_by(username=session['username']).first()
            if not user:
                app.logger.warning({
                    'event': 'user_not_found',
                    'username': session.get('username', 'unknown'),
                    'route': '/goals'
                })
                return redirect(url_for('login'))
            
            app.logger.info({
                'event': 'route_access',
                'route': '/goals',
                'username': session['username']
            })
            return render_template('goals.html', user=user)
        except Exception as e:
            current_app.logger.error({
                'event': 'goals_page_error',
                'message': f"An error occurred: {str(e)}"
            })
            return "An internal error occurred", 500

    @app.route('/foods')
    @login_required
    def food():
        try:
            app.logger.info({
                'event': 'route_access',
                'route': '/foods',
                'username': session.get('username', 'anonymous')
            })
            return render_template('foods.html')
        except Exception as e:
            current_app.logger.error({
                'event': 'foods_page_error',
                'message': f"An error occurred: {str(e)}"
            })
            return "An internal error occurred", 500

    @app.route('/activities')
    @login_required
    def activities():
        try:
            app.logger.info({
                'event': 'route_access',
                'route': '/activities',
                'username': session.get('username', 'anonymous')
            })
            return render_template('activities.html')
        except Exception as e:
            current_app.logger.error({
                'event': 'activities_page_error',
                'message': f"An error occurred: {str(e)}"
            })
            return "An internal error occurred", 500

    @app.route('/summary')
    @login_required
    def summary():
        try:
            app.logger.info({
                'event': 'route_access',
                'route': '/summary',
                'username': session.get('username', 'anonymous')
            })
            return render_template('summary.html')
        except Exception as e:
            current_app.logger.error({
                'event': 'summary_page_error',
                'message': f"An error occurred: {str(e)}"
            })
            return "An internal error occurred", 500

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        try:
            if request.method == 'POST':
                data = request.form
                username = data.get('username')
                password = data.get('password')
                
                if not username or not password:
                    current_app.logger.warning({
                        'event': 'login_attempt',
                        'message': 'Missing username or password',
                        'ip': request.remote_addr,
                        'status': 'failure'
                    })
                    return jsonify({'error': 'Username and password are required'}), 400

                user = User.query.filter_by(username=username).first()
                if user and check_password_hash(user.password_hash, password):
                    session['username'] = username
                    current_app.logger.info({
                        'event': 'login_success',
                        'message': f'User {username} logged in successfully',
                        'ip': request.remote_addr
                    })
                    return jsonify({'message': 'Successful login'}), 200
                else:
                    current_app.logger.warning({
                        'event': 'login_failure',
                        'message': 'Invalid username or password',
                        'username': username,
                        'ip': request.remote_addr
                    })
                    return jsonify({'error': 'Invalid username or password'}), 401
            current_app.logger.info({'event': 'render_login_page', 'message': 'Login page rendered'})
            return render_template('login.html')
        except Exception as e:
            current_app.logger.error({
                'event': 'login_error',
                'message': f"An error occurred during login: {str(e)}"
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500

    @app.route('/register', methods=['POST'])
    def register():
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            
            if not username or not password:
                return jsonify({'error': 'Username and password must be provided.'}), 400

            if User.query.filter_by(username=username).first():
                current_app.logger.warning({
                    'event': 'registration_attempt',
                    'message': f'Username {username} already exists',
                    'ip': request.remote_addr,
                    'status': 'failure'
                })
                return jsonify({'error': 'User already exists!'}), 400

            new_user = User(username=username, password_hash=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            current_app.logger.info({
                'event': 'registration_success',
                'message': f'User {username} registered successfully',
                'ip': request.remote_addr
            })
            return jsonify({'message': 'User registered successfully!'}), 201

        except ValidationError as err:
            current_app.logger.warning({
                'event': 'registration_attempt',
                'message': 'Invalid data provided',
                'ip': request.remote_addr,
                'errors': err.messages
            })
            return jsonify(err.messages), 400

        except Exception as e:
            current_app.logger.error({
                'event': 'registration_error',
                'message': f"An error occurred during registration: {str(e)}"
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500
        
    @app.route('/logout', methods=['POST'])
    def logout():
        try:
            username = session.pop('username', None)
            current_app.logger.info({
                'event': 'logout',
                'message': f'User {username} logged out',
                'ip': request.remote_addr
            })
            return jsonify({'message': 'Logged out successfully'}), 200
        except Exception as e:
            current_app.logger.error({
                'event': 'logout_error',
                'message': f"An error occurred during logout: {str(e)}"
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500

    @app.route('/api/update-goal', methods=['POST'])
    @login_required
    def update_goal():
        data = request.get_json()
        user = User.query.filter_by(username=session['username']).first()
        
        if not user:
            current_app.logger.error({
                'event': 'update_goal_failed',
                'message': 'User not found',
                'username': session.get('username'),
                'ip': request.remote_addr
            })
            return jsonify({'error': 'User not found'}), 404

        user.calorie_goal = data.get('calorie_goal', user.calorie_goal)
        user.protein_goal = data.get('protein_goal', user.protein_goal)
        user.fat_goal = data.get('fat_goal', user.fat_goal)
        user.carbs_goal = data.get('carbs_goal', user.carbs_goal)
        db.session.commit()
        
        current_app.logger.info({
            'event': 'update_goal',
            'message': 'User goals updated successfully',
            'username': session['username'],
            'ip': request.remote_addr
        })
        return jsonify({'message': 'Goals updated successfully!'}), 200

    @app.route('/api/food', methods=['POST'])
    @login_required
    def add_food():
        # Fetch the currently logged-in user
        user = User.query.filter_by(username=session['username']).first()
        if not user:
            current_app.logger.error({
                'event': 'add_food_failed',
                'message': 'User not found',
                'username': session.get('username'),
                'ip': request.remote_addr
            })
            return jsonify({'error': 'User not found'}), 404

        # Load the incoming JSON data
        incoming_data = request.get_json()

        # Prepare data for the schema load by adding user_id
        data = {
            'user_id': user.id,
            'date': incoming_data.get('date'),
            'food': incoming_data.get('food'),
            'calories': incoming_data.get('calories'),
            'protein': incoming_data.get('protein'),
            'fat': incoming_data.get('fat'),
            'carbs': incoming_data.get('carbs')
        }

        # Validate and deserialize the data
        schema = FoodLogSchema()
        try:
            validated_data = schema.load(data, session=db.session)

            # Validate required fields after loading
            if not validated_data.food or validated_data.calories is None or validated_data.protein is None \
                    or validated_data.fat is None or validated_data.carbs is None:
                current_app.logger.warning({
                    'event': 'add_food_failed',
                    'message': 'Missing food details',
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'Food name, calories, protein, fat, and carbs are required'}), 400

            # Create the new food log
            new_food_log = FoodLog(
                user_id=validated_data.user_id,
                date=validated_data.date,
                food=validated_data.food,
                calories=validated_data.calories,
                protein=validated_data.protein,
                fat=validated_data.fat,
                carbs=validated_data.carbs
            )

            # Add to the database and commit
            db.session.add(new_food_log)
            db.session.commit()

            current_app.logger.info({
                'event': 'add_food',
                'message': 'Food added successfully',
                'username': session['username'],
                'food': new_food_log.food,
                'ip': request.remote_addr
            })
            return jsonify({'message': 'Food added successfully!', 'id': new_food_log.id}), 201

        except ValidationError as err:
            current_app.logger.warning({
                'event': 'add_food_validation_failed',
                'errors': err.messages,
                'ip': request.remote_addr
            })
            return jsonify(err.messages), 400

        except Exception as e:
            current_app.logger.error({
                'event': 'add_food_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500
    
    @app.route('/api/food', methods=['DELETE'])
    @login_required
    def delete_food():
        try:
            data = request.get_json()
            food_id = data.get('food_id')
            
            if food_id is None:
                current_app.logger.warning({
                    'event': 'delete_food_failed',
                    'message': 'Food ID missing',
                    'request': data,
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'Food ID is required'}), 400
                
            food_log = FoodLog.query.get(food_id)
            
            if food_log: # and food_log.user.username == session['username']:
                db.session.delete(food_log)
                db.session.commit()
                current_app.logger.info({
                    'event': 'delete_food',
                    'message': 'Food deleted successfully',
                    'username': session['username'],
                    'food_id': food_id,
                    'ip': request.remote_addr
                })
                return jsonify({'message': 'Food deleted successfully!'}), 200

            current_app.logger.error({
                'event': 'delete_food_failed',
                'message': 'Food item not found or unauthorized',
                'username': session.get('username'),
                'food_id': food_id,
                'ip': request.remote_addr
            })
            return jsonify({'error': 'Food item not found!'}), 404

        except Exception as e:
            current_app.logger.error({
                'event': 'delete_food_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500

    @app.route('/api/fitness', methods=['POST'])
    @login_required
    def add_fitness():
        try:
            # Fetch the currently logged-in user
            user = User.query.filter_by(username=session['username']).first()
            if not user:
                current_app.logger.error({
                    'event': 'add_fitness_failed',
                    'message': 'User not found',
                    'username': session.get('username'),
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'User not found'}), 404

            # Load the incoming JSON data
            incoming_data = request.get_json()

            # Prepare data for the schema load by adding user_id
            data = {
                'user_id': user.id,  # Set user_id from the authenticated user
                'date': incoming_data.get('date'),
                'exercise': incoming_data.get('exercise'),
                'kcal_burned': incoming_data.get('kcal_burned')
            }

            # Validate and deserialize the data
            schema = FitnessLogSchema()
            validated_data = schema.load(data, session=db.session)  # Pass the modified data

            # Validate required fields after loading
            if not validated_data.exercise or validated_data.kcal_burned is None:
                current_app.logger.warning({
                    'event': 'add_fitness_failed',
                    'message': 'Missing fitness details',
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'Exercise and kcal burned are required'}), 400

            # Create a FitnessLog instance
            new_fitness_log = FitnessLog(
                user_id=validated_data.user_id,
                date=validated_data.date,
                exercise=validated_data.exercise,
                kcal_burned=validated_data.kcal_burned
            )

            # Add to the database and commit
            db.session.add(new_fitness_log)
            db.session.commit()

            current_app.logger.info({
                'event': 'add_fitness_success',
                'message': 'Exercise added successfully',
                'username': session['username'],
                'exercise': validated_data.exercise,
                'ip': request.remote_addr
            })
            return jsonify({'message': 'Exercise added successfully!', 'id': new_fitness_log.id}), 201


        except ValidationError as err:
            current_app.logger.warning({
                'event': 'add_fitness_validation_failed',
                'errors': err.messages,
                'ip': request.remote_addr
            })
            return jsonify(err.messages), 400

        except Exception as e:
            current_app.logger.error({
                'event': 'add_fitness_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500

    @app.route('/api/fitness', methods=['DELETE'])
    @login_required
    def delete_fitness():
        try:
            data = request.get_json()
            fitness_id = data.get('fitness_id')

            if fitness_id is None:
                current_app.logger.warning({
                    'event': 'delete_fitness_failed',
                    'message': 'Fitness ID missing',
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'Fitness ID is required'}), 400
                
            fitness_log = FitnessLog.query.get(fitness_id)
            
            if fitness_log: # and fitness_log.user.username == session['username']:
                db.session.delete(fitness_log)
                db.session.commit()
                current_app.logger.info({
                    'event': 'delete_fitness_success',
                    'message': 'Exercise deleted successfully',
                    'username': session['username'],
                    'fitness_id': fitness_id,
                    'ip': request.remote_addr
                })
                return jsonify({'message': 'Exercise deleted successfully!'}), 200

            current_app.logger.error({
                'event': 'delete_fitness_failed',
                'message': 'Exercise not found or unauthorized',
                'username': session.get('username'),
                'fitness_id': fitness_id,
                'ip': request.remote_addr
            })
            return jsonify({'error': 'Exercise not found!'}), 404

        except Exception as e:
            current_app.logger.error({
                'event': 'delete_fitness_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500

    @app.route('/daily-summary', methods=['GET'])
    @login_required
    def daily_summary():
        try:
            user = User.query.filter_by(username=session['username']).first()
            date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))

            if not user:
                current_app.logger.error({
                    'event': 'daily_summary_failed',
                    'message': 'User not found',
                    'username': session.get('username'),
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'User not found'}), 404

            food_log = FoodLog.query.filter_by(user_id=user.id, date=date).all()
            fitness_log = FitnessLog.query.filter_by(user_id=user.id, date=date).all()

            total_calories_consumed = sum(item.calories for item in food_log)
            total_calories_burned = sum(item.kcal_burned for item in fitness_log)
            total_protein = sum(item.protein for item in food_log)
            total_fat = sum(item.fat for item in food_log)
            total_carbs = sum(item.carbs for item in food_log)

            current_app.logger.info({
                'event': 'daily_summary',
                'message': 'Daily summary retrieved successfully',
                'username': session['username'],
                'date': date,
                'total_calories_consumed': total_calories_consumed,
                'total_calories_burned': total_calories_burned,
                'ip': request.remote_addr
            })

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

        except Exception as e:
            current_app.logger.error({
                'event': 'daily_summary_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500