# app/routes/routes_goals.py
from flask import render_template, redirect, url_for, request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.models import User, FoodLog, FitnessLog, UserSchema, FoodLogSchema, FitnessLogSchema
from .. import db
from functools import wraps
from datetime import datetime
from marshmallow import ValidationError
from .routes_auth import login_required

def init_goals_routes(app):
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