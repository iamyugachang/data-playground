import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POLARIS_URL = "http://data_playground_polaris:8181"
CLIENT_ID = "root"
CLIENT_SECRET = "s3cr3t"
CATALOG_NAME = "data_playground"

def get_token():
    url = f"{POLARIS_URL}/api/catalog/v1/oauth/tokens"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "PRINCIPAL_ROLE:ALL"
    }
    logger.info(f"Requesting token from {url}...")
    try:
        resp = requests.post(url, data=data)
        resp.raise_for_status()
        return resp.json()["access_token"]
    except Exception as e:
        logger.error(f"Error getting token: {e}")
        return None

def debug_api(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 1. List Catalogs
    logger.info("--- Listing Catalogs ---")
    resp = requests.get(f"{POLARIS_URL}/api/management/v1/catalogs", headers=headers)
    logger.info(f"Status: {resp.status_code}")
    logger.info(resp.text)

    # 2. List Principal Roles
    logger.info("--- Listing Principal Roles ---")
    resp = requests.get(f"{POLARIS_URL}/api/management/v1/principal-roles", headers=headers)
    logger.info(f"Status: {resp.status_code}")
    logger.info(resp.text)
    
    # 3. List Catalog Roles for data_playground
    logger.info(f"--- Listing Catalog Roles for {CATALOG_NAME} ---")
    resp = requests.get(f"{POLARIS_URL}/api/management/v1/catalogs/{CATALOG_NAME}/catalog-roles", headers=headers)
    logger.info(f"Status: {resp.status_code}")
    logger.info(resp.text)

    # 4. Try to add privilege with different structure
    role_name = "data_playground_admin"
    url_privs = f"{POLARIS_URL}/api/management/v1/catalogs/{CATALOG_NAME}/catalog-roles/{role_name}/grants"
    
    # Attempt 1: PUT with privilege (singular)
    payload1 = {
        "privilege": {
            "type": "CATALOG_MANAGE_CONTENT"
        }
    }
    logger.info(f"--- Attempting PUT grant with singular privilege ---")
    resp = requests.put(url_privs, json=payload1, headers=headers)
    logger.info(f"Status: {resp.status_code}")
    logger.info(resp.text)

    # Attempt 2: POST with privilege
    logger.info(f"--- Attempting POST grant ---")
    resp = requests.post(url_privs, json=payload1, headers=headers)
    logger.info(f"Status: {resp.status_code}")
    logger.info(resp.text)
    
    # 5. Try to assign role to principal role
    # Check if we can find a valid principal role first
    
    
if __name__ == "__main__":
    token = get_token()
    if token:
        debug_api(token)
