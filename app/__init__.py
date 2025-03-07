import time
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    from .models import User  # Import your User model

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Wait for MySQL to be ready
    with app.app_context():
        max_retries = 10
        retry_delay = 5  # seconds
        for attempt in range(1, max_retries + 1):
            try:
                # Test the database connection directly
                db.session.execute(text('SELECT 1'))
                db.create_all()
                print("✅ Database connection successful!")
                break
            except OperationalError as e:
                print(f"🔄 Attempt {attempt}/{max_retries}: Waiting for MySQL... ({e})")
                time.sleep(retry_delay)
        else:
            raise RuntimeError("❌ Failed to connect to MySQL after multiple retries")

    return app
