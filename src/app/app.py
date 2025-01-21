# app/app.py
from app import create_app
import logging
import os

app = create_app()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the Flask application")
    port = int(os.getenv('PORT', 8000))
    try:
        app.run(debug=False)
    finally:
        logging.info("Shutting down the Flask application")