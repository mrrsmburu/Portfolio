from flask import Blueprint, jsonify, request
from models.user import User
from extensions import db  # Import db from extensions

api_blueprint = Blueprint("api", __name__)

# Helper function to validate request data
def validate_fields(data, required_fields):
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
    return None

# Route: Get all users
@api_blueprint.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users]), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500

# Route: Submit a contact message
@api_blueprint.route("/contact", methods=["POST"])
def submit_contact():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["name", "email", "message"]
        validation_error = validate_fields(data, required_fields)
        if validation_error:
            return jsonify({"error": validation_error}), 400

        # Create new contact
        new_contact = User(
            name=data["name"],
            email=data["email"],
            message=data["message"]
        )
        db.session.add(new_contact)
        db.session.commit()
        
        return jsonify({
            "message": "Contact message sent successfully",
            "data": {"id": new_contact.id, "name": new_contact.name, "email": new_contact.email}
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to send contact message", "details": str(e)}), 500

# Route: Get all contact messages
@api_blueprint.route("/contact", methods=["GET"])
def get_contacts():
    try:
        contacts = User.query.all()
        return jsonify({
            "contacts": [{"id": contact.id, "name": contact.name, "email": contact.email, "message": contact.message} for contact in contacts]
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch contacts", "details": str(e)}), 500
