# app/routes/routes_goals.py
from flask import request, jsonify, session, current_app
from ..models.models import User, GoalsSchema
from .. import db
from marshmallow import ValidationError
from .routes_auth import login_required

# Function to initialize goal-related routes
def init_goals_routes(app):
    
    # Route to update user goals
    @app.route('/api/update-goal', methods=['POST'])
    @login_required  
    def update_goal():
        try:
            # Attempt to get JSON data from the request
            data = request.get_json()
            goals_schema = GoalsSchema()
            validated_data = goals_schema.load(data)

        except ValidationError as err:
            # Log the validation error details for debugging
            current_app.logger.error({
                'event': 'update_goal_failed',
                'message': 'Validation failed',
                'username': session.get('username'),
                'ip': request.remote_addr,
                'errors': err.messages
            })
            return jsonify({'errors': err.messages}), 400

        # Query the User model to find the currently logged-in user
        user = User.query.filter_by(username=session['username']).first()

        # If no user is found, log an error and return a 404 response
        if not user:
            current_app.logger.error({
                'event': 'update_goal_failed',
                'message': 'User not found',
                'username': session.get('username'),
                'ip': request.remote_addr
            })
            return jsonify({'error': 'User not found'}), 404

        # Update the user's goal data from the validated input
        user.calorie_goal = validated_data['calorie_goal']
        user.protein_goal = validated_data['protein_goal']
        user.fat_goal = validated_data['fat_goal']
        user.carbs_goal = validated_data['carbs_goal']

        # Commit the changes to the database
        db.session.commit()

        # Log a successful goal update
        current_app.logger.info({
            'event': 'update_goal',
            'message': 'User goals updated successfully',
            'username': session['username'],
            'ip': request.remote_addr
        })
        
        return jsonify({'message': 'Goals updated successfully!'}), 200