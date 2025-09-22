from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config  # relativo
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
    db.init_app(app)

    # imports relativos
    from .models.user import User
    from .routes import user_routes
    user_routes.register_user_routes(app)

    return app
