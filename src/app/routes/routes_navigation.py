# app/routes/routes_navigation.py
from flask import render_template, redirect, url_for, request, jsonify, session, current_app
from ..models.models import User
from .routes_auth import login_required

# Initialize routes for navigation within the application
def init_navigation_routes(app):

    # Route to serve the home page of the application
    @app.route('/')
    @login_required
    def home():
        try:
            # Log access to the route
            current_app.logger.info({
                'event': 'route_access',
                'route': '/',
                'username': session.get('username', 'anonymous'),
                'ip': request.remote_addr
            })
            return render_template('dashboard.html')
        except Exception as e:
            # Log any exceptions that occur and return an error message
            current_app.logger.error({
                'event': 'home_page_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return "An internal error occurred", 500

    # Route to serve the dashboard page
    @app.route('/dashboard')
    @login_required
    def dashboard():
        try:
            # Log access to the route
            current_app.logger.info({
                'event': 'route_access',
                'route': '/dashboard',
                'username': session.get('username', 'anonymous'),
                'ip': request.remote_addr
            })
            return render_template('dashboard.html')
        except Exception as e:
            # Log any exceptions that occur and return an error message
            current_app.logger.error({
                'event': 'dashboard_page_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return "An internal error occurred", 500

    # Route to manage and view user goals
    @app.route('/goals')
    @login_required
    def goals():
        try:
            # Fetch the user from the database using the session's username
            username = session.get('username', 'unknown')
            user = User.query.filter_by(username=username).first()

            if not user:
                # Log and redirect if user is not found
                current_app.logger.warning({
                    'event': 'user_not_found',
                    'username': username,
                    'route': '/goals',
                    'ip': request.remote_addr
                })
                return redirect(url_for('login'))

            # Log access to the route
            current_app.logger.info({
                'event': 'route_access',
                'route': '/goals',
                'username': username,
                'ip': request.remote_addr
            })
            return render_template('goals.html', user=user)
        except Exception as e:
            # Log any exceptions that occur and return an error message
            current_app.logger.error({
                'event': 'goals_page_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return "An internal error occurred", 500

    # Route to manage and view user food logs
    @app.route('/foods')
    @login_required
    def food():
        try:
            # Log access to the route
            current_app.logger.info({
                'event': 'route_access',
                'route': '/foods',
                'username': session.get('username', 'anonymous'),
                'ip': request.remote_addr
            })
            return render_template('foods.html')
        except Exception as e:
            # Log any exceptions that occur and return an error message
            current_app.logger.error({
                'event': 'foods_page_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return "An internal error occurred", 500

    # Route to manage and view user fitness activities
    @app.route('/activities')
    @login_required
    def activities():
        try:
            # Log access to the route
            current_app.logger.info({
                'event': 'route_access',
                'route': '/activities',
                'username': session.get('username', 'anonymous'),
                'ip': request.remote_addr
            })
            return render_template('activities.html')
        except Exception as e:
            # Log any exceptions that occur and return an error message
            current_app.logger.error({
                'event': 'activities_page_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return "An internal error occurred", 500

    # Route to view summary information
    @app.route('/summary')
    @login_required
    def summary():
        try:
            # Log access to the route
            current_app.logger.info({
                'event': 'route_access',
                'route': '/summary',
                'username': session.get('username', 'anonymous'),
                'ip': request.remote_addr
            })
            return render_template('summary.html')
        except Exception as e:
            # Log any exceptions that occur and return an error message
            current_app.logger.error({
                'event': 'summary_page_error',
                'message': f"An error occurred: {str(e)}",
                'ip': request.remote_addr
            })
            return "An internal error occurred", 500