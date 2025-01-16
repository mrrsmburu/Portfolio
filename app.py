from flask import Flask, jsonify, request
from extensions import db, migrate, cors
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app(test_config=None):
    """Application Factory to create and configure the Flask app."""
    app = Flask(__name__)
    
    # Set configuration
    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    else:
        app.config.update(test_config)
    
    # Initialize extensions
    db.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # Import models
        from models.user import User
        
        # Register blueprints
        try:
            from routes.api import api_blueprint
            app.register_blueprint(api_blueprint, url_prefix="/api")
        except ImportError:
            pass  # Handle case where routes aren't set up yet
        
        # Create database tables
        db.create_all()
    
    # Define frontend route equivalents
    @app.route("/home", methods=["GET"])
    def home():
        """Backend route for the Home page."""
        return jsonify({"message": "Welcome to the Home page!"})

    @app.route("/about", methods=["GET"])
    def about():
        """Backend route for the About page."""
        return jsonify({
            "message": "About Me",
            "content": "I'm a full-stack developer specializing in creating awesome web experiences."
        })

    @app.route("/services", methods=["GET"])
    def services():
        """Backend route for the Services page."""
        return jsonify({
            "message": "Our Services",
            "services": [
                {"id": 1, "title": "Web Development", "description": "Building responsive and dynamic websites."},
                {"id": 2, "title": "UI/UX Design", "description": "Crafting intuitive and visually appealing user experiences."},
                {"id": 3, "title": "Backend Development", "description": "Creating secure and robust server-side applications."}
            ]
        })

    @app.route("/portfolio", methods=["GET"])
    def portfolio():
        """Backend route for the Portfolio page."""
        return jsonify({
            "message": "My Portfolio",
            "projects": [
                {"id": 1, "name": "Project A", "description": "A cool project that does amazing things."},
                {"id": 2, "name": "Project B", "description": "A second project with even cooler features."}
            ]
        })

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        """Backend route for the Contact page."""
        if request.method == "GET":
            return jsonify({
                "message": "Contact Me",
                "email": "example@example.com",
                "phone": "+123456789",
                "address": "123 Developer Street, Code City"
            })
        elif request.method == "POST":
            try:
                data = request.get_json()
                # Validate required fields
                required_fields = ["name", "email", "message"]
                for field in required_fields:
                    if field not in data:
                        return jsonify({"error": f"Missing required field: {field}"}), 400
                
                # Save contact message to the database
                new_contact = User(name=data["name"], email=data["email"], message=data["message"])
                db.session.add(new_contact)
                db.session.commit()

                return jsonify({"message": "Contact message sent successfully"}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": "Failed to send message", "details": str(e)}), 500
    
    return app

# Only create app if this file is run directly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
else:
    app = create_app()
