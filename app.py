# from flask import Flask, render_template, request
# import pandas as pd


# app = Flask(__name__)


# @app.route('/')

# def index():
#     return render_template('index.html')


# @app.route("/home")
# def home():
#     return render_template('home.html')


# @app.route('/result', methods=["GET", 'POST'])

# def result():

#     source = str(request.form.get('source'))
#     destination = request.form.get('destination')

#     df = pd.read_csv("map_urls.csv")

#     print(source)
#     print(destination)

#     url = df[(df['SOURCE'] == source) & (
#         df['DESTINATION'] == destination)].reset_index().iloc[0]["MAP_URL"]

#     # url = url.encode("utf-8")

#     return render_template('result.html', iframe=url, source=source, destination=destination)


# if __name__ == "__main__":
#     app.run()
#     app.debug = True
# from flask import Flask, render_template, request, jsonify
# import csv
# import json
# import requests

# app = Flask(__name__)

# MAP_CSV = 'location_routes.csv'
# GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_API_KEY"

# Load CSV into memory
# def load_routes():
#     routes = []
#     with open(MAP_CSV, newline='', encoding='utf-8') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             routes.append(row)
#     return routes

# routes_data = load_routes()

# @app.route('/')
# def index():
#     return render_template('index.html')
# @app.route('/home')
# def home():
#     return render_template('home.html')

# @app.route('/result', methods=["GET",'POST'])
# def result():
#     source = request.form.get('source')
#     destination = request.form.get('destination')

#     # Find matching route from CSV
#     match = next(
#         (r for r in routes_data if r['SOURCE'] == source and r['DESTINATION'] == destination),
#         None
#     )

#     if match:
#         map_url = match['MAP_URL']
#         return render_template('result.html', source=source, destination=destination, iframe=map_url)
#     else:
#         return render_template('error.html', message="Route not found", source=source, destination=destination)


# # New API to get navigation instructions (for AR overlay)
# @app.route('/api/directions', methods=['POST'])
# def get_directions():
#     data = request.json
#     origin = data.get("origin")
#     destination = data.get("destination")

#     url = (
#         f"https://maps.googleapis.com/maps/api/directions/json?"
#         f"origin={origin['lat']},{origin['lng']}&"
#         f"destination={destination['lat']},{destination['lng']}&"
#         f"mode=walking&key={GOOGLE_MAPS_API_KEY}"
#     )

#     response = requests.get(url)
#     directions = response.json()
#     return jsonify(directions)


# if __name__ == "__main__":
#     app.run(debug=True, port=5000)


from flask import Flask, render_template, request, jsonify
import csv
import json
import requests
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_CSV = os.path.join(BASE_DIR, 'location_routes.csv')



def load_routes():
    routes = []
    with open(MAP_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            routes.append(row)
    return routes

routes_data = load_routes()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
   return render_template('home.html')

@app.route('/result2', methods=['POST'])
def result():
    source = request.form.get('source')
    destination = request.form.get('destination')

    # Find matching route from CSV
    match = next(
        (r for r in routes_data if r['SOURCE'] == source and r['DESTINATION'] == destination),
        None
    )

    if match:

        # Minimal: pull destination coordinates from CSV row (adjust names if your CSV differs)
        # Expect columns like LAT2 and LON2 in your CSV for destination coordinates
        dest_lat = match.get('LAT2') or match.get('DEST_LAT') or match.get('DESTINATION_LAT')
        dest_lng = match.get('LON2') or match.get('DEST_LON') or match.get('DESTINATION_LON')

        # convert to float when available
        try:
            if dest_lat: dest_lat = float(dest_lat)
            if dest_lng: dest_lng = float(dest_lng)
        except Exception:
            dest_lat = None
            dest_lng = None

        return render_template(
            'result2.html',
            source=source,
            destination=destination,
            iframe=map_url,
            dest_lat=dest_lat,
            dest_lng=dest_lng
        )
    else:
        return render_template('error.html', message="Route not found", source=source, destination=destination)


# New API to get navigation instructions (for AR overlay) using OSRM (no API key)
@app.route('/api/directions', methods=['POST'])
def get_directions():
    data = request.json
    origin = data.get("origin")
    destination = data.get("destination")

    if not origin or not destination:
        return jsonify({"error": "origin and destination required"}), 400

    # OSRM public server route query (walking)
    osrm_url = (
        f"https://router.project-osrm.org/route/v1/foot/"
        f"{origin['lng']},{origin['lat']};{destination['lng']},{destination['lat']}"
        f"?overview=full&geometries=geojson&steps=true"
    )

    resp = requests.get(osrm_url, timeout=10)
    return jsonify(resp.json())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
