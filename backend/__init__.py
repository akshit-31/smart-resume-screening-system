from flask import Flask
from backend.config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('/tmp/flask_sessions', exist_ok=True)

    from backend.routes.pages import pages_bp
    from backend.routes.upload import upload_bp
    from backend.routes.match import match_bp
    from backend.routes.results import results_bp
    from backend.routes.resume_view import resume_view_bp
    from backend.routes.roast import roast_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(results_bp)
    app.register_blueprint(resume_view_bp)
    app.register_blueprint(roast_bp)

    return app
