from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Data file kept next to this script so the path works on any host
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'cooler_data.json')

# Default cooler data (used only when cooler_data.json does not exist yet)
cooler_data = {
    "location01A": {
        "title": "01 : Floor-G, Left",
        "video": "https://www.youtube.com/embed/tgbNymZ7vqY",
        "waterLevel": "0",
        "roTds": "105",
        "safety": "Green",
        "waterTemp": "0",
        "systemWorking": "OK"
    },
    "location01B": {
        "title": "02 : Floor-G, Right",
        "video": "https://www.youtube.com/embed/5qap5aO4i9A",
        "waterLevel": "25",
        "roTds": "105",
        "safety": "Red",
        "waterTemp": "5",
        "systemWorking": "OK"
    },
    "location02A": {
        "title": "03 : Floor-1, Left",
        "video": "https://www.youtube.com/embed/tgbNymZ7vqY",
        "waterLevel": "50",
        "roTds": "105",
        "safety": "Yellow",
        "waterTemp": "10",
        "systemWorking": "Not OK"
    },
    "location02B": {
        "title": "04 : Floor-1, Right",
        "video": "https://www.youtube.com/embed/5qap5aO4i9A",
        "waterLevel": "100",
        "roTds": "105",
        "safety": "Green",
        "waterTemp": "15",
        "systemWorking": "Not OK"
    },
    "location03A": {
        "title": "05 : Floor-2, Left",
        "video": "https://www.youtube.com/embed/tgbNymZ7vqY",
        "waterLevel": "150",
        "roTds": "105",
        "safety": "Green",
        "waterTemp": "25",
        "systemWorking": "OK"
    },
    "location03B": {
        "title": "06 : Floor-2, Right",
        "video": "https://www.youtube.com/embed/5qap5aO4i9A",
        "waterLevel": "200",
        "roTds": "105",
        "safety": "Green",
        "waterTemp": "30",
        "systemWorking": "OK"
    },
    "location04A": {
        "title": "07 : Floor-3, Left",
        "video": "https://www.youtube.com/embed/tgbNymZ7vqY",
        "waterLevel": "250",
        "roTds": "105",
        "safety": "Green",
        "waterTemp": "5",
        "systemWorking": "Not OK"
    },
    "location04B": {
        "title": "08 : Floor-3, Right",
        "video": "https://www.youtube.com/embed/5qap5aO4i9A",
        "waterLevel": "300",
        "roTds": "105",
        "safety": "Green",
        "waterTemp": "25",
        "systemWorking": "Not OK"
    }
}


def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(cooler_data, f, indent=2)


def load_data():
    global cooler_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            cooler_data = json.load(f)
        print("Data loaded from file")
    else:
        save_data()
        print("Created new data file")


load_data()


@app.route('/')
def home():
    return '<h1>Welcome to NeerNetra IoT API!</h1>'


@app.route('/api/coolers', methods=['GET'])
def get_coolers():
    return jsonify(cooler_data)


@app.route('/api/coolers/<location_id>', methods=['GET'])
def get_cooler(location_id):
    if location_id in cooler_data:
        return jsonify(cooler_data[location_id])
    return jsonify({"error": "Cooler not found"}), 404


@app.route('/api/coolers/<location_id>', methods=['PUT', 'POST'])
def update_cooler(location_id):
    """Update specific cooler fields, including roTds"""
    if location_id not in cooler_data:
        return jsonify({"error": "Cooler not found"}), 404

    try:
        data = request.get_json()
        allowed_fields = ['waterLevel', 'safety', 'waterTemp', 'systemWorking', 'roTds']
        for field in allowed_fields:
            if field in data:
                cooler_data[location_id][field] = str(data[field])

        save_data()
        return jsonify({
            "status": "success",
            "location": location_id,
            "updated_data": cooler_data[location_id]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/coolers/<location_id>/roTds', methods=['POST'])
def update_rotds(location_id):
    """Quick update for roTds only"""
    if location_id not in cooler_data:
        return jsonify({"error": "Cooler not found"}), 404

    try:
        data = request.get_json()
        rotds = data.get('roTds')
        if rotds is None:
            return jsonify({"error": "roTds required"}), 400

        cooler_data[location_id]['roTds'] = str(rotds)
        save_data()
        return jsonify({
            "status": "success",
            "location": location_id,
            "roTds": rotds
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    # Local testing only. On Render, gunicorn runs the app.
    app.run()
