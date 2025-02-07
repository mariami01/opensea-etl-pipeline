from etl_pipeline import extract_opensea_collections, transform_collections_data
from database import load_data_to_db
import os
import json

def save_raw_data(raw_data, filename="data/raw_collections.json"):
    """
    Saves raw API data into a JSON file inside the 'data' directory.
    """
    os.makedirs("data", exist_ok=True)
    with open(filename, "w") as file:
        json.dump(raw_data, file, indent=4)
    print(f"Raw data saved to {filename}")

if __name__ == "__main__":
    print("Starting ETL pipeline.")
    raw_data = extract_opensea_collections()
    if raw_data:
        save_raw_data(raw_data)
        transformed_data = transform_collections_data(raw_data)
        print(f"🔍 Preview of Transformed Data (First 3 Records): {transformed_data[:3]}")
        load_data_to_db(transformed_data)

    print("ETL pipeline completed successfully!!!! :)")
