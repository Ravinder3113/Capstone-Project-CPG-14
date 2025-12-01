from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timezone
import mysql.connector
import traceback

app = Flask(__name__)
CORS(app)

# ---- MYSQL CONFIG ----
db = mysql.connector.connect(
    host="localhost",
    user="anpr_user",
    password="ANPR_STRONG_PASSWORD",
    database="anpr_mysql"
)
cursor = db.cursor()

API_KEY = "MY_SECRET_KEY_123"   # Same as used in Colab OCR sender


# --------------------------------
# AUTH CHECK
# --------------------------------
def authorized(req):
    key = req.headers.get("X-API-KEY")
    return key == API_KEY


# --------------------------------
# INSERT PLATE FROM OCR
# --------------------------------
@app.route("/plates", methods=["POST"])
def save_plate():
    if not authorized(request):
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    data = request.get_json()

    if not data or "plate" not in data:
        return jsonify({"ok": False, "error": "invalid payload"}), 400

    plate = data["plate"]
    timestamp = data.get("timestamp")
    location = data.get("location")
    latitude = float(data["latitude"])
    longitude = float(data["longitude"])

    try:
        sql = """
            INSERT INTO numberplate
            (plate, timestamp, location, latitude, longitude, location_point)
            VALUES (%s, %s, %s, %s, %s, ST_SRID(Point(%s, %s), 4326))
        """
        vals = (plate, timestamp, location, latitude, longitude,
                longitude, latitude)

        cursor.execute(sql, vals)
        db.commit()

        return jsonify({"ok": True}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"ok": False, "error": str(e)}), 500


# --------------------------------
# EXPORT AS GEOJSON FOR QGIS
# --------------------------------
@app.route("/geojson", methods=["GET"])
def geojson():
    cursor.execute("""
        SELECT plate, timestamp, location,
               ST_X(location_point), ST_Y(location_point)
        FROM numberplate
        WHERE location_point IS NOT NULL
    """)

    features = []
    for plate, ts, loc, lon, lat in cursor.fetchall():

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "plate": plate,
                "timestamp": ts.isoformat() if ts else None,
                "location": loc
            }
        })

    return jsonify({
        "type": "FeatureCollection",
        "features": features
    })


if __name__ == "__main__":
    print("Server running at http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)