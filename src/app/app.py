# app/app.py
from app import create_app
import logging

app = create_app()

if __name__ == '__main__':
    logging.info("Starting the Flask application")
    try:
        app.run(debug=True)
    finally:
        logging.info("Shutting down the Flask application")