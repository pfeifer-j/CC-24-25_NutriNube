# app/routes/routes_food.py
from flask import jsonify, request, session, current_app
from ..models.models import User, FoodLog, FoodLogSchema
from .. import db
from .routes_auth import login_required
from marshmallow import ValidationError

# Initialize routes related to food logs
def init_food_routes(app):

    # Route to handle adding a new food log
    @app.route('/api/food', methods=['POST'])
    @login_required
    def add_food():
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            # Log error if the user is not found
            current_app.logger.error({
                'event': 'add_food_failed',
                'message': 'User not found',
                'username': username,
                'ip': request.remote_addr
            })
            return jsonify({'error': 'User not found'}), 404

        # Load incoming JSON data from the request
        incoming_data = request.get_json()
        if incoming_data is None:
            current_app.logger.warning({
                'event': 'add_food_failed',
                'message': 'Invalid or missing JSON',
                'ip': request.remote_addr
            })
            return jsonify({'error': 'Invalid or missing JSON'}), 400

        # Add user_id to data to associate it with the correct user
        data = {'user_id': user.id, **incoming_data}

        # Validate and deserialize the data
        schema = FoodLogSchema()
        try:
            # Load and validate the data using the schema
            validated_food_log = schema.load(data, session=db.session)

            # Add the validated food log to the database and commit
            db.session.add(validated_food_log)
            db.session.commit()

            # Log success and return response
            current_app.logger.info({
                'event': 'add_food_success',
                'message': 'Food added successfully',
                'username': username,
                'food': validated_food_log.food,
                'ip': request.remote_addr
            })
            return jsonify({'message': 'Food added successfully!', 'id': validated_food_log.id}), 201

        except ValidationError as err:
            # Log validation errors and return them as response
            current_app.logger.warning({
                'event': 'add_food_validation_failed',
                'errors': err.messages,
                'ip': request.remote_addr
            })
            return jsonify(err.messages), 400

        except Exception as e:
            # Log unexpected exceptions and return a generic error
            current_app.logger.error({
                'event': 'add_food_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500

    # Route to handle deleting an existing food log
    @app.route('/api/food', methods=['DELETE'])
    @login_required
    def delete_food():
        username = session.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            # Log error if user is not found
            current_app.logger.error({
                'event': 'delete_food_failed',
                'message': 'User not found',
                'username': username,
                'ip': request.remote_addr
            })
            return jsonify({'error': 'User not found'}), 404

        try:
            # Load and validate incoming JSON data
            data = request.get_json()
            if data is None:
                current_app.logger.warning({
                    'event': 'delete_food_failed',
                    'message': 'Missing JSON data',
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'Invalid or missing JSON data'}), 400

            # Extract food ID from the request
            food_id = data.get('food_id')
            if not food_id:
                current_app.logger.warning({
                    'event': 'delete_food_failed',
                    'message': 'Food ID missing',
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'Food ID is required'}), 400

            # Fetch the food log using db.session.get()
            food_log = db.session.get(FoodLog, food_id)

            # Check log ownership and perform deletion if authorized
            if food_log and food_log.user_id == user.id:
                db.session.delete(food_log)
                db.session.commit()
                current_app.logger.info({
                    'event': 'delete_food_success',
                    'message': 'Food deleted successfully',
                    'username': username,
                    'food_id': food_id,
                    'ip': request.remote_addr
                })
                return jsonify({'message': 'Food deleted successfully!'}), 200

            # Log error if the log was not found or user is unauthorized
            current_app.logger.error({
                'event': 'delete_food_failed',
                'message': 'Food item not found or unauthorized',
                'username': username,
                'food_id': food_id,
                'ip': request.remote_addr
            })
            return jsonify({'error': 'Food item not found or unauthorized'}), 404

        except Exception as e:
            # Log unexpected exceptions and return a generic error
            current_app.logger.error({
                'event': 'delete_food_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500