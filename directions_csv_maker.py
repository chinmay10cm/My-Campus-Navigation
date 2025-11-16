import pandas as pd
from itertools import permutations
import os

def generate_location_pairs(input_excel, output_csv):
    """
    Generate all possible location pairs from the input Excel file.
    
    Args:
        input_excel (str): Path to the input Excel file
        output_csv (str): Path to save the output CSV file
    """
    try:
        # Read the Excel file
        df = pd.read_excel(input_excel)
        print("Successfully read the Excel file.")
        print("Columns found:", df.columns.tolist())
        
        # Check if required columns exist
        required_cols = ["Location", "Latitude", "Longitude"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns in Excel: {missing_cols}")
        
        # Get unique locations
        locations = df.drop_duplicates(subset=['Location']).to_dict('records')
        print(f"Found {len(locations)} unique locations.")
        
        # Generate all possible pairs (both directions)
        pairs = list(permutations(locations, 2))
        print(f"Generated {len(pairs)} location pairs.")
        
        # Prepare output data
        output_rows = []
        for loc1, loc2 in pairs:
            row = {
                "Source": loc1["Location"],
                "Destination": loc2["Location"],
                "Source_Lat": loc1["Latitude"],
                "Source_Lon": loc1["Longitude"],
                "Dest_Lat": loc2["Latitude"],
                "Dest_Lon": loc2["Longitude"]
            }
            output_rows.append(row)
        
        # Create and save DataFrame
        output_df = pd.DataFrame(output_rows)
        output_df.to_csv(output_csv, index=False)
        
        print(f"\nSuccessfully generated {len(output_df)} location pairs.")
        print(f"CSV saved to: {os.path.abspath(output_csv)}")
        
        # Print sample of the generated data
        print("\nSample of generated data:")
        print(output_df.head().to_string(index=False))
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease check the input file format. It should have columns: Location, Latitude, Longitude")
        print("Example row: {'Location': 'LRC', 'Latitude': 28.51914, 'Longitude': 77.36536}")

if __name__ == "__main__":
    # Use the new locations file we created
    input_excel = os.path.join(os.path.dirname(__file__), "campus_locations.xlsx")
    output_csv = os.path.join(os.path.dirname(__file__), "location_routes.csv")
    
    print(f"Input file: {os.path.abspath(input_excel)}")
    print(f"Output file: {os.path.abspath(output_csv)}\n")
    
    generate_location_pairs(input_excel, output_csv)
