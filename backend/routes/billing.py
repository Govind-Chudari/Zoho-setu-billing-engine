from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from services.billing_service import (
    calculate_bill,
    generate_invoice,
    get_current_estimate,
    get_user_invoices,
    mark_invoice_paid
)
from datetime import date

billing_bp = Blueprint("billing", __name__)


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))


# current month live preview
@billing_bp.route("/api/billing/estimate", methods=["GET"])
@jwt_required()
def estimate():
    """
    Live estimate of what this month's bill will be.
    Includes a forecast for the full month.
    Frontend shows this as 'Estimated Bill This Month'.
    """
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = get_current_estimate(user.id)

    return jsonify({
        "username": user.username,
        "estimate": data
    }), 200


# CALCULATE — preview bill (month)
@billing_bp.route("/api/billing/calculate", methods=["GET"])
@jwt_required()
def calculate():
    """
    Calculates (but does NOT save) the bill for any month.
    Use this to preview before generating a real invoice.

    ?year=2026&month=2
    """
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    today = date.today()
    try:
        year  = int(request.args.get("year",  today.year))
        month = int(request.args.get("month", today.month))

        if month < 1 or month > 12:
            return jsonify({"error": "month must be between 1 and 12"}), 400

    except ValueError:
        return jsonify({"error": "year and month must be valid numbers"}), 400

    bill = calculate_bill(user.id, year, month)

    return jsonify({
        "username": user.username,
        "bill":     bill
    }), 200


# create and save an invoice
@billing_bp.route("/api/billing/generate", methods=["POST"])
@jwt_required()
def generate():
    """
    Generates a real invoice and saves it to the database.
    Body: { "year": 2026, "month": 2 }

    If invoice already exists for that month, returns it without duplicating.
    """
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data  = request.get_json() or {}
    today = date.today()

    try:
        year  = int(data.get("year",  today.year))
        month = int(data.get("month", today.month))

        if month < 1 or month > 12:
            return jsonify({"error": "month must be between 1 and 12"}), 400

    except (ValueError, TypeError):
        return jsonify({"error": "year and month must be valid numbers"}), 400

    result      = generate_invoice(user.id, year, month)
    status_code = 200 if result["already_existed"] else 201

    return jsonify({
        "username": user.username,
        **result
    }), status_code


# LIST — all invoices 
@billing_bp.route("/api/billing/invoices", methods=["GET"])
@jwt_required()
def list_invoices():
    """
    Returns all saved invoices for the current user.
    Shows total amount spent across all months.
    """
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = get_user_invoices(user.id)

    return jsonify({
        "username": user.username,
        **data
    }), 200


# GET single invoice by ID
@billing_bp.route("/api/billing/invoices/<int:invoice_id>", methods=["GET"])
@jwt_required()
def get_invoice(invoice_id):
    """
    Returns a single invoice.
    Users can only see their own invoices.
    """
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    from models import Invoice
    invoice = Invoice.query.filter_by(
        id=invoice_id,
        user_id=user.id
    ).first()

    if not invoice:
        return jsonify({
            "error": f"Invoice #{invoice_id} not found",
            "hint":  "Use GET /api/billing/invoices to see your invoices"
        }), 404

    return jsonify({
        "username": user.username,
        "invoice":  invoice.to_dict()
    }), 200


# Mark invoice as paid
@billing_bp.route("/api/billing/invoices/<int:invoice_id>/pay", methods=["POST"])
@jwt_required()
def pay_invoice(invoice_id):
    """
    Marks an invoice as paid.
    In a real system this would integrate with Razorpay/Stripe.
    For now it just updates the status.
    """
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    invoice, message = mark_invoice_paid(invoice_id, user.id)

    if not invoice:
        return jsonify({"error": message}), 404

    return jsonify({
        "message":  message,
        "invoice":  invoice.to_dict()
    }), 200