# coral_agents.py
from flood_agent import flood_agent
from safety_agent import safety_agent
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/flood_risk", methods=["GET"])
def get_flood_risk():
    place = request.args.get("place_name")
    if not place:
        return jsonify({"error": "Missing place_name"}), 400
    data = flood_agent(place)
    return jsonify(data)

@app.route("/safety", methods=["GET"])
def get_safety():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Missing lat or lon"}), 400
    data = safety_agent(float(lat), float(lon))
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
