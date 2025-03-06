import time
from flask import request, jsonify
from app import supabase
from app.middleware.session import token_required 

from . import vehicles_bp

@vehicles_bp.route("/create", methods=["POST"])
@token_required
def create_vehicle():
    """
    Create a new vehicle for the authenticated user.
    Expects: multipart/form-data with:
        - vehicle_number: str (required)
        - type: str (required)
        - name: str (required)
        - color: str (required)
        - image: file (optional)
    Returns: Vehicle details.
    """
    print(f"Content-Type: {request.content_type}")
    required_fields = ["vehicle_number", "type", "name", "color"]
    for field in required_fields:
        if field not in request.form:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    try:
        user = supabase.auth.get_user()
        vehicle_number = request.form["vehicle_number"]
        vehicle_type = request.form["type"]
        name = request.form["name"]
        color = request.form["color"]
        
        vehicle_photo_url = ""
        if "image" in request.files:
            image = request.files["image"]
            if image.filename:
                file_path = f"{user.user.id}/{vehicle_number}_{int(time.time())}.jpg"
                print(f"Uploading vehicle image to: {file_path}")
                supabase.storage.from_("vehicle_pictures").upload(file_path, image.read(), file_options={"content-type": image.mimetype})
                vehicle_photo_url = supabase.storage.from_("vehicle_pictures").get_public_url(file_path)
                print(f"Vehicle image URL: {vehicle_photo_url}")
            else:
                print("No image file selected, proceeding without image.")
        else:
            print("No image provided, proceeding without image.")
        
        vehicle_data = {
            "user_id": user.user.id,
            "vehicle_number": vehicle_number,
            "type": vehicle_type,
            "name": name,
            "color": color,
            "vehicle_photo": vehicle_photo_url if vehicle_photo_url else "defaultVehicleImage",
            "created_at": "now()"
        }
        response = supabase.table("vehicles").insert(vehicle_data).execute()
        
        # Update user's vehicles array
        user_profile = supabase.table("users").select("vehicles").eq("id", user.user.id).single().execute()
        # Ensure current_vehicles is a list, even if vehicles is NULL
        current_vehicles = user_profile.data.get("vehicles") or []
        if not isinstance(current_vehicles, list):
            current_vehicles = []
        current_vehicles.append(response.data[0]["id"])
        supabase.table("users").update({"vehicles": current_vehicles}).eq("id", user.user.id).execute()
        
        return jsonify({"message": "Vehicle created successfully", "vehicle": response.data[0]}), 201
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 400

@vehicles_bp.route("/user", methods=["GET"])
@token_required
def get_user_vehicles():
    """
    Get all vehicles for the authenticated user.
    Returns: List of vehicles.
    """
    try:
        user = supabase.auth.get_user()
        vehicles = supabase.table("vehicles").select("*").eq("user_id", user.user.id).execute()
        return jsonify({"vehicles": vehicles.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500