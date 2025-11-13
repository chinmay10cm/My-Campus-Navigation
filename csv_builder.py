import csv

# Define your key campus locations (name → coordinates)
locations = {
    "home": {"lat": 28.637205, "lng": 77.361294},
    "main gate": {"lat": 28.636852, "lng": 77.360709},

}

# Generate all source-destination pairs
rows = []
for source_name, source_coords in locations.items():
    for dest_name, dest_coords in locations.items():
        if source_name != dest_name:
            map_url = (
                f"https://www.google.com/maps/embed/v1/directions?"
                f"key=YOUR_GOOGLE_API_KEY&origin={source_coords['lat']},{source_coords['lng']}"
                f"&destination={dest_coords['lat']},{dest_coords['lng']}&mode=walking"
            )

            rows.append({
                "SOURCE": source_name,
                "DESTINATION": dest_name,
                "MAP_URL": map_url,
                "LAT1": source_coords["lat"],
                "LON1": source_coords["lng"],
                "LAT2": dest_coords["lat"],
                "LON2": dest_coords["lng"]
            })

# Write the CSV file
with open("map_direction.csv", "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = ["SOURCE", "DESTINATION", "MAP_URL", "LAT1", "LON1", "LAT2", "LON2"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Generated map_urls.csv with {len(rows)} routes successfully!")
