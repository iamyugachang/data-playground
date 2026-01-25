import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use old URL for now to debug running container
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
    
    role_name = "data_playground_admin"
    principal_role = "service_admin"

    # 1. Try GET grants
    logger.info(f"--- GET Grants for {role_name} ---")
    url_get_grants = f"{POLARIS_URL}/api/management/v1/catalogs/{CATALOG_NAME}/catalog-roles/{role_name}/grants"
    resp = requests.get(url_get_grants, headers=headers)
    logger.info(f"Status: {resp.status_code}")
    logger.info(resp.text)

    # 2. Try POST grant with simpler payload
    logger.info(f"--- Attempting PUT grant with list ---")
    payload_list = {
        "privileges": [
            {
                "type": "CATALOG_MANAGE_CONTENT"
            }
        ]
    }
    # Original script did PUT with this list and got 400. Let's try POST.
    resp = requests.post(url_get_grants, json=payload_list, headers=headers)
    logger.info(f"Status (POST list): {resp.status_code}")
    logger.info(resp.text)

    # Try payload without wrapper?
    logger.info(f"--- Attempting POST grant without wrapper ---")
    payload_raw = {"type": "CATALOG_MANAGE_CONTENT"}
    resp = requests.post(url_get_grants, json=payload_raw, headers=headers)
    logger.info(f"Status (POST raw): {resp.status_code}")
    logger.info(resp.text)

    # 3. Try Assignment: Principal Role -> Catalog Role (POST)
    url_assign = f"{POLARIS_URL}/api/management/v1/principal-roles/{principal_role}/catalog-roles/{CATALOG_NAME}/{role_name}"
    logger.info(f"--- Attempting Assignment (POST) ---")
    resp = requests.post(url_assign, headers=headers)
    logger.info(f"Trying URL: {url_assign}")
    logger.info(f"Status: {resp.status_code}")
    logger.info(resp.text)

if __name__ == "__main__":
    token = get_token()
    if token:
        debug_api(token)
