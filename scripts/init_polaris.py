import requests
import time
import sys

POLARIS_URL = "http://dbt_playground_polaris:8181"
CLIENT_ID = "root"
CLIENT_SECRET = "s3cr3t"
CATALOG_NAME = "dbt_playground"

def get_token():
    url = f"{POLARIS_URL}/api/catalog/v1/oauth/tokens"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "PRINCIPAL_ROLE:ALL"
    }
    print(f"Requesting token from {url}...")
    try:
        resp = requests.post(url, data=data)
        resp.raise_for_status()
        return resp.json()["access_token"]
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def create_catalog(token):
    url = f"{POLARIS_URL}/api/management/v1/catalogs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": CATALOG_NAME,
        "type": "INTERNAL",
        "readOnly": False,
        "properties": {
            "default-base-location": "s3://warehouse/"
        },
        "storageConfigInfo": {
            "storageType": "S3",
            "allowedLocations": ["s3://warehouse/"]
        }
    }
    
    print(f"Creating catalog '{CATALOG_NAME}'...")
    try:
        resp = requests.post(url, json=payload, headers=headers)
        if resp.status_code == 409:
            print("Catalog already exists.")
            return True
        resp.raise_for_status()
        print("Catalog created successfully.")
        return True
    except Exception as e:
        print(f"Error creating catalog: {e}")
        print(resp.text)
        return False

def main():
    # Wait for Polaris to be ready
    for i in range(30):
        token = get_token()
        if token:
            if create_catalog(token):
                print("Initialization complete.")
                break
        print("Waiting for Polaris...")
        time.sleep(2)

if __name__ == "__main__":
    main()
