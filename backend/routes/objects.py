from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, StorageObject, UsageLog
from services.minio_service import (
    upload_file, download_file, delete_file,
    list_files, get_total_storage_used
)
from datetime import datetime, date
import io

objects_bp = Blueprint("objects", __name__)


def get_current_user():
    """Helper — gets the logged-in User object from the database"""
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))


def log_api_call(user_id):
    """
    Every time a user makes an API call, we record it.
    This is how we count API calls for billing later.
    """
    today = date.today()
    log = UsageLog.query.filter_by(user_id=user_id, date=today).first()

    if log:
        log.api_calls += 1
    else:
        log = UsageLog(user_id=user_id, date=today, api_calls=1, storage_used=0)
        db.session.add(log)

    db.session.commit()


def update_storage_log(user_id, username):
    """
    After every upload/delete, update today's storage snapshot.
    """
    today = date.today()
    total_bytes = get_total_storage_used(username)

    log = UsageLog.query.filter_by(user_id=user_id, date=today).first()
    if log:
        log.storage_used = total_bytes
    else:
        log = UsageLog(user_id=user_id, date=today, storage_used=total_bytes, api_calls=0)
        db.session.add(log)

    db.session.commit()


# UPLOAD a file
@objects_bp.route("/api/objects/upload", methods=["POST"])
@jwt_required()
def upload():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if a file was sent in the request
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "File has no name"}), 400

    file_data     = file.read()
    filename      = file.filename
    content_type  = file.content_type or "application/octet-stream"
    file_size     = len(file_data)

    # Check if file with same name already exists for this user
    existing = StorageObject.query.filter_by(
        user_id=user.id, filename=filename
    ).first()
    if existing:
        return jsonify({"error": f"File '{filename}' already exists. Delete it first or rename your file."}), 409

    # Upload to MinIO
    success = upload_file(user.username, file_data, filename, content_type, file_size)

    if not success:
        return jsonify({"error": "Upload failed — MinIO error"}), 500

    # Save file record in database
    new_object = StorageObject(
        user_id=user.id,
        filename=filename,
        object_key=f"{user.username}/{filename}",
        file_size=file_size
    )
    db.session.add(new_object)
    db.session.commit()

    # Log the API call and update storage
    log_api_call(user.id)
    update_storage_log(user.id, user.username)

    return jsonify({
        "message": f"File '{filename}' uploaded successfully!",
        "file": new_object.to_dict()
    }), 201


# LIST all files for the logged-in user
@objects_bp.route("/api/objects/list", methods=["GET"])
@jwt_required()
def list_user_files():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    log_api_call(user.id)

    # Get files from database
    db_files = StorageObject.query.filter_by(user_id=user.id).all()

    total_size_bytes = sum(f.file_size for f in db_files)

    return jsonify({
        "username": user.username,
        "total_files": len(db_files),
        "total_size_kb": round(total_size_bytes / 1024, 2),
        "total_size_mb": round(total_size_bytes / (1024 * 1024), 4),
        "files": [f.to_dict() for f in db_files]
    }), 200


# DOWNLOAD a file
@objects_bp.route("/api/objects/download/<filename>", methods=["GET"])
@jwt_required()
def download(filename):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check file belongs to this user
    obj = StorageObject.query.filter_by(user_id=user.id, filename=filename).first()
    if not obj:
        return jsonify({"error": f"File '{filename}' not found"}), 404

    log_api_call(user.id)

    # Get file bytes from MinIO
    file_data = download_file(user.username, filename)

    if file_data is None:
        return jsonify({"error": "File not found in storage"}), 404

    return send_file(
        io.BytesIO(file_data),
        download_name=filename,
        as_attachment=True
    )


# DELETE a file
@objects_bp.route("/api/objects/<filename>", methods=["DELETE"])
@jwt_required()
def delete(filename):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check file belongs to this user
    obj = StorageObject.query.filter_by(user_id=user.id, filename=filename).first()
    if not obj:
        return jsonify({"error": f"File '{filename}' not found"}), 404

    # Delete from MinIO
    success = delete_file(user.username, filename)
    if not success:
        return jsonify({"error": "Delete failed — MinIO error"}), 500

    # Delete from database
    db.session.delete(obj)
    db.session.commit()

    # Update storage log
    log_api_call(user.id)
    update_storage_log(user.id, user.username)

    return jsonify({"message": f"File '{filename}' deleted successfully!"}), 200