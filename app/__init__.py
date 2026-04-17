from flask import Flask
from app.config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from app.routes.upload import upload_bp
    from app.routes.match import match_bp
    from app.routes.results import results_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(results_bp)

    return app
