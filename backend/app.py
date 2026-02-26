from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config
from models import db
from routes.auth import auth_bp, bcrypt
from routes.objects import objects_bp 
from routes.usage   import usage_bp 
from routes.billing import billing_bp 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(objects_bp)
    app.register_blueprint(usage_bp) 
    app.register_blueprint(billing_bp)

    with app.app_context():
        db.create_all()
        print("✅ Database tables created!")

    @app.route("/")
    def home():
        return jsonify({
            "message": "Billing Engine API is running! 🚀",
            "endpoints": {
                "auth":    ["/api/register", "/api/login", "/api/profile"],
                "objects": ["/api/objects/upload", "/api/objects/list",
                            "/api/objects/download/<file>", "/api/objects/<file>"],
                "usage":   ["/api/usage/today", "/api/usage/history",
                            "/api/usage/current-month", "/api/usage/monthly"],
                "billing": ["/api/billing/estimate", "/api/billing/calculate",
                            "/api/billing/generate", "/api/billing/invoices"]
            }
        }), 200
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)