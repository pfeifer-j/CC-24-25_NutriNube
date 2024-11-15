# app/routes/routes_fitness.py
from flask import render_template, redirect, url_for, request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.models import User, FoodLog, FitnessLog, UserSchema, FoodLogSchema, FitnessLogSchema
from .. import db
from functools import wraps
from datetime import datetime
from marshmallow import ValidationError
from .routes_auth import login_required

def init_fitness_routes(app):
    
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

            # Prepare data for the schema load
            data = {
                'user_id': user.id,
                'date': incoming_data.get('date'),
                'exercise': incoming_data.get('exercise'),
                'kcal_burned': incoming_data.get('kcal_burned')
            }

            # Validate and deserialize the data
            schema = FitnessLogSchema()
            validated_data = schema.load(data, session=db.session) 

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