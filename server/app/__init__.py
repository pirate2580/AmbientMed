from flask import Flask
from app.controllers.appointment_controller import appointment_bp

def create_app():
    app = Flask(__name__)
    # Register Blueprints
    app.register_blueprint(appointment_bp, url_prefix='/appointments')

    return app