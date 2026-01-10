# dbt Trino Iceberg Playground

This project demonstrates an ETL pipeline using dbt, Trino, Iceberg (MinIO), and Postgres.

## Architecture

*   **Trino**: Query engine acting as the transformation layer.
*   **Postgres**: Source database (Shop data).
*   **MinIO**: Object storage for Iceberg tables.
*   **Hive Metastore**: Managing Iceberg metadata.
*   **dbt**: Managing transformations and documentation.

## Setup

1.  **Start Services**:
    ```bash
    docker compose up -d
    ```

2.  **Wait for services**:
    Wait a minute for Trino and Hive Metastore to fully start.

3.  **Initialize Iceberg Data**:
    Run the initialization script to create the `iceberg.data.events` table and populate it with sample data.
    ```bash
    docker compose exec trino trino -f /scripts/init_iceberg.sql
    ```

4.  **Run dbt**:
    Compile and run the dbt models.
    ```bash
    docker compose exec dbt dbt deps
    docker compose exec dbt dbt debug
    docker compose exec dbt dbt run
    ```

5.  **View Docs**:
    Generate and serve the dbt documentation.
    ```bash
    docker compose exec dbt dbt docs generate
    docker compose exec dbt dbt docs serve --port 8081 --host 0.0.0.0
    ```
    Access docs at [http://localhost:8081](http://localhost:8081).

## Data Scenario

*   **Source 1 (Postgres)**: `shop.public.customers`, `shop.public.products`.
*   **Source 2 (Iceberg)**: `iceberg.data.events`.
*   **Target (Trino View)**: `dbt_playground.marts.customer_activity`.
