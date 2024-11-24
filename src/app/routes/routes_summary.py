# app/routes/routes_summary.py
from flask import jsonify, request, session, current_app
from ..models.models import User, FoodLog, FitnessLog
from .. import db
from .routes_auth import login_required
from datetime import datetime

# Initialize routes related to the daily summary feature
def init_summary_routes(app):

    # Route to retrieve a daily summary of user activities and consumption
    @app.route('/daily-summary', methods=['GET'])
    @login_required
    def daily_summary():
        try:
            # Retrieve the user from the session and ensure they exist
            username = session.get('username')
            user = User.query.filter_by(username=username).first()

            # Get the date from request parameters or default to today's date
            date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))

            if not user:
                # Log an error if the user is not found
                current_app.logger.error({
                    'event': 'daily_summary_failed',
                    'message': 'User not found',
                    'username': username,
                    'ip': request.remote_addr
                })
                return jsonify({'error': 'User not found'}), 404

            # Query for food and fitness logs for the given date
            food_log = FoodLog.query.filter_by(user_id=user.id, date=date).all()
            fitness_log = FitnessLog.query.filter_by(user_id=user.id, date=date).all()

            # Calculate summary statistics
            total_calories_consumed = sum(item.calories for item in food_log)
            total_calories_burned = sum(item.kcal_burned for item in fitness_log)
            total_protein = sum(item.protein for item in food_log)
            total_fat = sum(item.fat for item in food_log)
            total_carbs = sum(item.carbs for item in food_log)

            # Log the successful retrieval of the summary
            current_app.logger.info({
                'event': 'daily_summary_success',
                'message': 'Daily summary retrieved successfully',
                'username': username,
                'date': date,
                'total_calories_consumed': total_calories_consumed,
                'total_calories_burned': total_calories_burned,
                'ip': request.remote_addr
            })

            # Return the summary data as JSON
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
            # Log any exceptions and return a generic error message
            current_app.logger.error({
                'event': 'daily_summary_error',
                'message': f"An error occurred: {str(e)}",
                'username': session.get('username', 'unknown'),
                'ip': request.remote_addr
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500