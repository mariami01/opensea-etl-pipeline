import os
import requests
from dotenv import load_dotenv
import json 
import pandas as pd 


load_dotenv()
API_KEY = os.getenv("OPENSEA_API_KEY")

def extract_opensea_collections():
    """
    Extracts collections data from OpenSea API for the Ethereum blockchain.
    Handles errors and returns data if successful.
    """
    url = "https://api.opensea.io/api/v2/collections"
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY 
    }
    params = {
        "chain": "ethereum" 
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json() 
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None 

def transform_collections_data(data):
    """
    Cleans and structures OpenSea collections data.
    - Removes duplicates
    - Replaces missing values with "N/A"
    - Ensures valid URLs
    - Extracts first Ethereum contract
    - Standardizes owner names
    - Removes collections with missing critical fields
    """
    if not data or "collections" not in data:
        print("❌ No collections found in API response.")
        return []

    transformed = []
    seen_collections = set() 

    for collection in data["collections"]:
        slug = collection.get("slug", "").strip().lower()
        name = collection.get("name", "").strip()
        description = collection.get("description", "").strip()

        if not slug or slug == "n/a":
            slug = name.lower().replace(" ", "-") if name else "unnamed-collection"

        if not name or name.lower() == "n/a":
            name = slug.replace("-", " ").title()

        if not description or description.lower() == "n/a":
            description = "No description provided for this collection."

        image_url = collection.get("image_url", "").strip()
        owner = collection.get("owner", "").strip().lower()
        twitter_username = collection.get("twitter_username", "").strip().lower()

        contracts_list = collection.get("contracts", [])
        ethereum_contracts = [c["address"].lower() for c in contracts_list if c["chain"] == "ethereum"]
        first_contract = ethereum_contracts[0] if ethereum_contracts else "No Ethereum Contract"

        if not image_url.startswith("https://"):
            image_url = "No Image Available"

        if not twitter_username:
            twitter_username = "No Twitter"

        if first_contract == "No Ethereum Contract":
            continue  

        if slug in seen_collections:
            continue  
        seen_collections.add(slug)

        transformed.append({
            "collection": slug,
            "name": name,
            "description": description,
            "image_url": image_url,
            "owner": owner,
            "twitter_username": twitter_username,
            "contracts": first_contract, 
        })

    df = pd.DataFrame(transformed)
    df.drop_duplicates(subset=["collection"], keep="first", inplace=True)

    return df.to_dict(orient="records")


def save_raw_data(raw_data, filename="data/raw_collections.json"):
    """
    Saves raw API data into a JSON file inside the 'data' directory.
    """
    os.makedirs("data", exist_ok=True) 
    with open(filename, "w") as file:
        json.dump(raw_data, file, indent=4)
    print(f"Raw data saved to {filename}")
