from flask import request, jsonify
from app import supabase
from app.middleware.session import token_required  # Updated import

from . import trips_bp

@trips_bp.route("/create", methods=["POST"])
@token_required
def create_trip():
    """
    Create a new ride.
    Expects: {
        "pick_up_address": str,
        "drop_off_address": str,
        "pick_up_lat": float,
        "pick_up_long": float,
        "dropoff_lat": float,
        "dropoff_long": float,
        "date_time": str (ISO format),
        "seats": int,
        "vehicle_id": str (optional),
        "cost": float (optional)
    }
    Returns: Trip details.
    """
    data = request.get_json()
    required_fields = ["pick_up_address", "drop_off_address", "pick_up_lat", "pick_up_long", "dropoff_lat", "dropoff_long", "date_time", "seats"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        user = supabase.auth.get_user()
        trip_data = {
            "creator_id": user.user.id,
            "vehicle_id": data.get("vehicle_id"),  # Optional
            "pick_up_address": data["pick_up_address"],
            "drop_off_address": data["drop_off_address"],
            "pick_up_lat": float(data["pick_up_lat"]),
            "pick_up_long": float(data["pick_up_long"]),
            "dropoff_lat": float(data["dropoff_lat"]),
            "dropoff_long": float(data["dropoff_long"]),
            "date_time": data["date_time"],
            "seats": int(data["seats"]),
            "passengers": [],  # Initialize as empty list
            "created_at": "now()"
        }
        if "cost" in data:
            trip_data["cost"] = float(data["cost"])
        
        response = supabase.table("trips").insert(trip_data).execute()
        return jsonify({"message": "Trip created successfully", "trip": response.data[0]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@trips_bp.route("/join", methods=["POST"])
@token_required
def join_trip():
    """
    Join an existing ride.
    Expects: {"trip_id": str}
    Returns: Success message or error.
    """
    data = request.get_json()
    if "trip_id" not in data:
        return jsonify({"error": "Missing trip_id"}), 400
    
    try:
        user = supabase.auth.get_user()
        trip_id = data["trip_id"]
        
        # Fetch trip to check seats
        trip = supabase.table("trips").select("*").eq("id", trip_id).single().execute()
        if not trip.data or int(trip.data["seats"]) <= 0:
            return jsonify({"error": "No available seats"}), 400
        
        # Add user to passengers
        passenger_id = user.user.id
        current_passengers = trip.data.get("passengers", [])
        if passenger_id not in current_passengers:
            current_passengers.append(passenger_id)
            supabase.table("trips").update({
                "seats": int(trip.data["seats"]) - 1,
                "passengers": current_passengers
            }).eq("id", trip_id).execute()
        
        return jsonify({"message": "Joined trip successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400