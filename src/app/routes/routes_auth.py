# app/routes/routes_auth.py
from flask import render_template, redirect, url_for, request, jsonify, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.models import User
from .. import db
from functools import wraps
from marshmallow import ValidationError

# Utility decorator to enforce login on certain routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is in the session, redirect to login if not
        if 'username' not in session:
            current_app.logger.info({
                'event': 'access_denied',
                'message': 'User attempted to access a protected route without logging in',
                'route': request.path
            })
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize routes related to authentication
def init_auth_routes(app):
    
    # Route to handle login requests
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        try:
            if request.method == 'POST':
                data = request.form
                username = data.get('username')
                password = data.get('password')

                # Check if both username and password were provided
                if not username or not password:
                    current_app.logger.warning({
                        'event': 'login_attempt',
                        'message': 'Missing username or password',
                        'ip': request.remote_addr,
                        'status': 'failure'
                    })
                    return jsonify({'error': 'Username and password are required'}), 400

                # Query the database for the provided username
                user = User.query.filter_by(username=username).first()

                # Authenticate user by checking password hash
                if user and check_password_hash(user.password_hash, password):
                    session['username'] = username
                    current_app.logger.info({
                        'event': 'login_success',
                        'message': f'User {username} logged in successfully',
                        'ip': request.remote_addr
                    })
                    return jsonify({'message': 'Successful login'}), 200
                else:
                    current_app.logger.warning({
                        'event': 'login_failure',
                        'message': 'Invalid username or password',
                        'username': username,
                        'ip': request.remote_addr
                    })
                    return jsonify({'error': 'Invalid username or password'}), 401

            # Render the login page
            current_app.logger.info({'event': 'render_login_page', 'message': 'Login page rendered'})
            return render_template('login.html')
        except Exception as e:
            current_app.logger.error({
                'event': 'login_error',
                'message': f"An error occurred during login: {str(e)}"
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500

    # Route to handle user registration
    @app.route('/register', methods=['POST'])
    def register():
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            # Ensure username and password are provided
            if not username or not password:
                current_app.logger.warning({
                    'event': 'registration_attempt',
                    'message': 'Missing username or password',
                    'ip': request.remote_addr,
                    'status': 'failure'
                })
                return jsonify({'error': 'Username and password must be provided.'}), 400

            # Check if the username is already taken
            if User.query.filter_by(username=username).first():
                current_app.logger.warning({
                    'event': 'registration_attempt',
                    'message': f'Username {username} already exists',
                    'ip': request.remote_addr,
                    'status': 'failure'
                })
                return jsonify({'error': 'User already exists!'}), 400

            # Create a new user and save to the database
            new_user = User(username=username, password_hash=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            current_app.logger.info({
                'event': 'registration_success',
                'message': f'User {username} registered successfully',
                'ip': request.remote_addr
            })
            return jsonify({'message': 'User registered successfully!'}), 201

        except ValidationError as err:
            current_app.logger.warning({
                'event': 'registration_attempt',
                'message': 'Invalid data provided',
                'ip': request.remote_addr,
                'errors': err.messages
            })
            return jsonify(err.messages), 400

        except Exception as e:
            current_app.logger.error({
                'event': 'registration_error',
                'message': f"An error occurred during registration: {str(e)}"
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500

    # Route to handle user logout
    @app.route('/logout', methods=['POST'])
    def logout():
        try:
            username = session.pop('username', None)
            current_app.logger.info({
                'event': 'logout',
                'message': f'User {username} logged out',
                'ip': request.remote_addr
            })
            return jsonify({'message': 'Logged out successfully'}), 200
        except Exception as e:
            current_app.logger.error({
                'event': 'logout_error',
                'message': f"An error occurred during logout: {str(e)}"
            })
            return jsonify({'error': 'An unexpected error occurred'}), 500