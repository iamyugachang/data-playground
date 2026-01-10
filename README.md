# dbt Trino Iceberg Playground (with Apache Polaris)

This project demonstrates an ETL pipeline using dbt, Trino, Iceberg (MinIO), Apache Polaris, and Postgres.

## Architecture

*   **Trino**: Query engine acting as the transformation layer.
*   **Postgres**: Source database (Shop data).
*   **MinIO**: Object storage for Iceberg tables.
*   **Apache Polaris**: Iceberg REST Catalog for metadata management.
*   **dbt**: Managing transformations and documentation.

## Setup

1.  **Start Services**:
    ```bash
    docker compose up -d --build
    ```

2.  **Initialize Polaris Catalog**:
    Wait for Polaris (port 8181) to be ready, then run the initialization script. This script creates the `dbt_playground` catalog in Polaris.
    ```bash
    docker compose exec dbt_playground_dbt_runner python3 /scripts/init_polaris.py
    ```

3.  **Initialize Iceberg Data**:
    Run the SQL script to create the `iceberg.data.events` table in Trino (which talks to Polaris -> MinIO).
    ```bash
    docker compose exec dbt_playground_trino trino -f /scripts/init_iceberg.sql
    ```

4.  **Run dbt**:
    Compile and run the dbt models.
    ```bash
    docker compose exec dbt_playground_dbt_runner dbt deps
    docker compose exec dbt_playground_dbt_runner dbt debug
    docker compose exec dbt_playground_dbt_runner dbt run
    ```

5.  **View Docs**:
    Generate and serve the dbt documentation.
    ```bash
    docker compose exec dbt_playground_dbt_runner dbt docs generate
    docker compose exec dbt_playground_dbt_runner dbt docs serve --port 8081 --host 0.0.0.0
    ```
    Access docs at [http://localhost:8081](http://localhost:8081).

## Data Scenario

*   **Source 1 (Postgres)**: `shop.public.customers`, `shop.public.products`.
*   **Source 2 (Iceberg)**: `iceberg.data.events`.
*   **Target (Trino View)**: `dbt_playground.marts.customer_activity`.
