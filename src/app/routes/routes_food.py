# app/routes/routes_food.py
from flask import render_template, redirect, url_for, request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.models import User, FoodLog, FitnessLog, UserSchema, FoodLogSchema, FitnessLogSchema
from .. import db
from functools import wraps
from datetime import datetime
from marshmallow import ValidationError
from .routes_auth import login_required

def init_food_routes(app):
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
