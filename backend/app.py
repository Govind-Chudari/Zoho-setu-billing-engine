from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS 
from config import Config
from models import db
from routes.auth import auth_bp, bcrypt
from routes.objects import objects_bp 
from routes.usage   import usage_bp 
from routes.billing import billing_bp 
from routes.admin   import admin_bp 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=["http://localhost:3000"])

    db.init_app(app)
    JWTManager(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(objects_bp)
    app.register_blueprint(usage_bp) 
    app.register_blueprint(billing_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        print("Database tables created!")

    @app.route("/")
    def home():
        return jsonify({"message": "Billing Engine API is running! "})
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)