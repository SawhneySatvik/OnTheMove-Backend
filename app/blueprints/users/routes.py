from flask import jsonify, request
from app import supabase
from functools import wraps
from app.middleware.session import token_required
from . import users_bp

@users_bp.route("/profile", methods=["GET"])
@token_required
def get_profile():
    """
    Fetch the authenticated user's profile.
    Returns: User profile data.
    """
    try:
        user = supabase.auth.get_user()
        profile = supabase.table("users").select("*").eq("id", user.user.id).single().execute()
        return jsonify(profile.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile():
    """
    Update the authenticated user's profile.
    Expects: JSON with fields to update (e.g., name, phone, institute).
    Returns: Success message.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    allowed_fields = ["name", "phone", "age", "gender", "institute", "profile_picture"]
    update_data = {key: str(data[key]) if key == "phone" else data[key] for key in data if key in allowed_fields}
    
    try:
        user = supabase.auth.get_user()
        supabase.table("users").update(update_data).eq("id", user.user.id).execute()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@users_bp.route("/profile/picture", methods=["POST"])
@token_required
def upload_profile_picture():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    try:
        user = supabase.auth.get_user()
        file_path = f"{user.user.id}/profile.jpg"
        print(f"Attempting upload to: {file_path}")
        
        upload_response = supabase.storage.from_("profile_pictures").upload(file_path, image.read(), file_options={"content-type": image.mimetype})
        print(f"Upload response: {upload_response}")
        
        public_url = supabase.storage.from_("profile_pictures").get_public_url(file_path)
        print(f"Public URL: {public_url}")
        
        print(f"Updating user {user.user.id} in public.users with profile_picture: {public_url}")
        update_response = supabase.table("public.users").update({"profile_picture": public_url}).eq("id", user.user.id).execute()
        print(f"Update response: {update_response}")
        
        return jsonify({"message": "Profile picture uploaded", "url": public_url}), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500