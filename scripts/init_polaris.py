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

def configure_rbac(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 1. Create catalog role 'dbt_admin'
    role_name = "dbt_admin"
    url_role = f"{POLARIS_URL}/api/management/v1/catalogs/{CATALOG_NAME}/catalog-roles"
    payload_role = {"name": role_name}
    print(f"Creating catalog role '{role_name}'...")
    try:
        resp = requests.post(url_role, json=payload_role, headers=headers)
        if resp.status_code == 409:
            print(f"Catalog role '{role_name}' already exists.")
        elif resp.status_code == 201:
            print(f"Catalog role '{role_name}' created.")
        else:
            print(f"Failed to create role: {resp.text}")
    except Exception as e:
        print(f"Error creating role: {e}")

    # 2. Grant privileges to 'dbt_admin'
    # Use 'grants' endpoint instead of 'privileges'
    url_privs = f"{POLARIS_URL}/api/management/v1/catalogs/{CATALOG_NAME}/catalog-roles/{role_name}/grants"
    payload_privs = {
        "privileges": [
            {"type": "CATALOG_MANAGE_CONTENT"}
        ]
    }
    print(f"Granting privileges to '{role_name}'...")
    try:
        resp = requests.put(url_privs, json=payload_privs, headers=headers)
        if resp.status_code in [200, 201, 204]:
             print(f"Privileges granted to '{role_name}'.")
        else:
             print(f"Failed to grant privileges: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Error granting privileges: {e}")

    # 3. Assign 'dbt_admin' to principal role 'service_admin'
    # Try assigning to principal role 'service_admin'
    principal_role = "service_admin"
    url_grant_role = f"{POLARIS_URL}/api/management/v1/catalogs/{CATALOG_NAME}/catalog-roles/{role_name}/grants/principal-roles/{principal_role}"
    print(f"Assigning '{role_name}' to principal role '{principal_role}'...")
    try:
        resp = requests.put(url_grant_role, headers=headers)
        if resp.status_code in [200, 201, 204]:
             print(f"Role assigned to principal role '{principal_role}'.")
        else:
             print(f"Failed to assign to principal role: {resp.status_code} {resp.text}")
             
             # Fallback: Try assigning to Principal 'root'
             principal_name = "root"
             url_grant_principal = f"{POLARIS_URL}/api/management/v1/catalogs/{CATALOG_NAME}/catalog-roles/{role_name}/grants/principals/{principal_name}" # Guessing endpoint
             print(f"Attempting fallback: Assigning '{role_name}' to principal '{principal_name}'...")
             resp2 = requests.put(url_grant_principal, headers=headers)
             if resp2.status_code in [200, 201, 204]:
                 print(f"Role assigned to principal '{principal_name}'.")
             else:
                 print(f"Failed to assign to principal: {resp2.status_code} {resp2.text}")

    except Exception as e:
        print(f"Error assigning role: {e}")

def main():
    # Wait for Polaris to be ready
    for i in range(30):
        token = get_token()
        if token:
            if create_catalog(token):
                configure_rbac(token)
                print("Initialization complete.")
                break
        print("Waiting for Polaris...")
        time.sleep(2)

if __name__ == "__main__":
    main()
