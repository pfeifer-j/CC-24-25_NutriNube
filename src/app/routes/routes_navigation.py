# app/routes/routes_navigation.py
from flask import render_template, redirect, url_for, request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.models import User, FoodLog, FitnessLog, UserSchema, FoodLogSchema, FitnessLogSchema
from .. import db
from functools import wraps
from datetime import datetime
from marshmallow import ValidationError
from .routes_auth import login_required

def init_navigation_routes(app):
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