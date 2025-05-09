# Backend - main.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Configurations
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "super-secret-key-please-change") # Ensure this is changed via ENV VAR
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///p2p_lending.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import and register blueprints after app, db, and jwt are initialized
from src.routes.user_routes import user_bp
from src.models.models import User, Loan, LenderPreference
app.register_blueprint(user_bp, url_prefix="/api")

@app.route("/")
def hello():
    return "Backend is running!"

# Ensure database tables are created
# This will run when the application starts
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # This block is for local development run (e.g., python src/main.py)
    # For production, Gunicorn will be used and it won't run this __main__ block directly,
    # but the db.create_all() above will still execute when the app/module is loaded.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
