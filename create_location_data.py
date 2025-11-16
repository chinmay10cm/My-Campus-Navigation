import pandas as pd

# Sample location data with coordinates
location_data = [
    {"Location": "LRC", "Latitude": 28.51914, "Longitude": 77.36536},
    {"Location": "Gate 1", "Latitude": 28.51969, "Longitude": 77.36489},
    {"Location": "MPH", "Latitude": 28.51972, "Longitude": 77.36528},
    {"Location": "Gate 2", "Latitude": 28.51861, "Longitude": 77.36481},
    {"Location": "Main Ground", "Latitude": 28.51917, "Longitude": 77.36611},
    {"Location": "Football Ground", "Latitude": 28.51778, "Longitude": 77.36500},
    {"Location": "Mess", "Latitude": 28.52000, "Longitude": 77.36667},
    {"Location": "Cafe", "Latitude": 28.51833, "Longitude": 77.36556}
]

# Create DataFrame
df = pd.DataFrame(location_data)

# Save to Excel
df.to_excel("campus_locations.xlsx", index=False)
print("Location data saved to 'campus_locations.xlsx'")
