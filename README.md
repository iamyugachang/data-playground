# Data Playground (Trino, Iceberg, Polaris, dbt)

This project demonstrates an ETL pipeline using dbt, Trino, Iceberg (MinIO), Apache Polaris, and Postgres. It is structured as a "Demonstration Hub" monorepo.

## Architecture

*   **Trino**: Query engine acting as the transformation layer.
*   **Postgres**: Source database (Shop data).
*   **MinIO**: Object storage for Iceberg tables.
*   **Apache Polaris**: Iceberg REST Catalog for metadata management.
*   **dbt**: Managing transformations and documentation.

## Repository Structure

*   `apps/`: Contains application code.
    *   `dbt-analytics/`: The main dbt project.
*   `infrastructure/`: Configuration for infrastructure services.
    *   `trino`, `postgres`, `polaris`, `dbt/docker`, `dbt/profiles`.
*   `scripts/`: Shared initialization and utility scripts.

## Setup

1.  **Start Services**:
    ```bash
    docker compose up -d --build
    ```

2.  **Initialize Polaris Catalog**:
    Wait for Polaris (port 8181) to be ready, then run the initialization script. This script creates the `data_playground` catalog in Polaris.
    ```bash
    docker compose exec dbt python3 /scripts/init_polaris.py
    ```

3.  **Initialize MinIO Bucket**:
    Create the `warehouse` bucket in MinIO.
    ```bash
    docker compose exec dbt python3 /scripts/init_minio.py
    ```

4.  **Initialize Iceberg Data**:
    Run the SQL script to create the `iceberg.data.events` table in Trino (which talks to Polaris -> MinIO).
    ```bash
    # Load Iceberg Data (Trino)
    docker compose exec dbt dbt seed --target dev --select iceberg

    # Load Shop Data (Postgres)
    docker compose exec dbt dbt seed --target shop --select shop
    ```
    *(Note: Using dbt seeds for data loading as per previous configuration)*

5.  **Run dbt**:
    Compile and run the dbt models.
    ```bash
    docker compose exec dbt dbt deps
    docker compose exec dbt dbt debug
    docker compose exec dbt dbt run
    ```

6.  **View Docs**:
    The dbt documentation is automatically served at [http://localhost:8081](http://localhost:8081).
    To update the docs after running models:
    ```bash
    # Try generating manually if needed, though container does it on start
    docker compose exec dbt dbt docs generate
    ```
    Then refresh your browser.

## Data Scenario

*   **Source 1 (Postgres)**: `shop.public.customers`, `shop.public.products`.
*   **Source 2 (Iceberg)**: `iceberg.data.events`.
*   **Target (Trino View)**: `data_playground.marts.customer_activity`.
