# app/routes/routes_summary.py
from flask import render_template, redirect, url_for, request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.models import User, FoodLog, FitnessLog, UserSchema, FoodLogSchema, FitnessLogSchema
from .. import db
from functools import wraps
from datetime import datetime
from marshmallow import ValidationError
from .routes_auth import login_required

def init_summary_routes(app):
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