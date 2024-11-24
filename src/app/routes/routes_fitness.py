# app/routes/routes_fitness.py
from flask import jsonify, request, session, current_app
from ..models.models import User, FitnessLog, FitnessLogSchema
from .. import db
from marshmallow import ValidationError
from .routes_auth import login_required

# Initialize routes related to fitness logs
def init_fitness_routes(app):

    # Route to handle adding a new fitness log
    @app.route('/api/fitness', methods=['POST'])
    @login_required
    def add_fitness():
        try:
            # Fetch the currently logged-in user
            user = User.query.filter_by(username=session['username']).first()
            if not user:
                # Log error if the user is not found in the session
                current_app.logger.error({
                    'event': 'add_fitness_failed',
                    'message': 'User not found',
                    'username': session.get('username'),
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'User not found'}), 404

            # Load incoming JSON data from request
            incoming_data = request.get_json()

            # Prepare data for the schema load
            data = {
                'user_id': user.id,
                'date': incoming_data.get('date'),
                'exercise': incoming_data.get('exercise'),
                'kcal_burned': incoming_data.get('kcal_burned')
            }

            # Validate and deserialize the data using the schema
            schema = FitnessLogSchema()
            validated_data = schema.load(data, session=db.session)

            # Create a new FitnessLog instance and store in the database
            new_fitness_log = FitnessLog(
                user_id=validated_data.user_id,
                date=validated_data.date,
                exercise=validated_data.exercise,
                kcal_burned=validated_data.kcal_burned
            )
            db.session.add(new_fitness_log)
            db.session.commit()

            # Log success and return response
            current_app.logger.info({
                'event': 'add_fitness_success',
                'message': 'Exercise added successfully',
                'username': session['username'],
                'exercise': validated_data.exercise,
                'ip': request.remote_addr
            })
            return jsonify({'message': 'Exercise added successfully!', 'id': new_fitness_log.id}), 201

        except ValidationError as err:
            # Log validation failure and return errors
            current_app.logger.warning({
                'event': 'add_fitness_validation_failed',
                'errors': err.messages,
                'ip': request.remote_addr
            })
            return jsonify(err.messages), 400

        except Exception as e:
            # Log unexpected exceptions and return a generic error
            current_app.logger.error({
                'event': 'add_fitness_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500

    # Route to handle deleting an existing fitness log
    @app.route('/api/fitness', methods=['DELETE'])
    @login_required
    def delete_fitness():
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            # Log error if user is not found
            current_app.logger.error({
                'event': 'delete_fitness_failed',
                'message': 'User not found',
                'username': session.get('username'),
                'ip': request.remote_addr
            })
            return jsonify({'error': 'User not found'}), 404

        try:
            # Load and check incoming JSON data
            data = request.get_json()
            if data is None:
                current_app.logger.warning({
                    'event': 'delete_fitness_failed',
                    'message': 'Missing JSON data',
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'Invalid or missing JSON data'}), 400

            # Extract fitness ID from the request
            fitness_id = data.get('fitness_id')
            if not fitness_id:
                current_app.logger.warning({
                    'event': 'delete_fitness_failed',
                    'message': 'Fitness ID missing',
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'Fitness ID is required'}), 400

            # Fetch the fitness log using the session
            fitness_log = db.session.get(FitnessLog, fitness_id)

            # Check log ownership and perform deletion if authorized
            if fitness_log and fitness_log.user_id == user.id:
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

            # Log error if the log was not found or user is unauthorized
            current_app.logger.error({
                'event': 'delete_fitness_failed',
                'message': 'Exercise not found or unauthorized',
                'username': session.get('username'),
                'fitness_id': fitness_id,
                'ip': request.remote_addr
            })
            return jsonify({'error': 'Exercise not found or unauthorized'}), 404

        except Exception as e:
            # Log unexpected exceptions and return a generic error
            current_app.logger.error({
                'event': 'delete_fitness_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500