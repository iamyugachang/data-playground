# dbt Trino Iceberg Playground

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

2.  **Initialize Infrastructure**:
    Wait for Polaris (port 8181) to be ready, then run the initialization scripts.
    ```bash
    docker compose exec dbt python3 /scripts/init_polaris.py
    docker compose exec dbt python3 /scripts/init_minio.py
    ```

3.  **Initialize Data (dbt Seeds)**:
    Load sample data into Iceberg and Postgres using dbt seeds.
    ```bash
    # Load Iceberg Data (Trino)
    docker compose exec dbt dbt seed --target dev --select iceberg

    # Load Shop Data (Postgres)
    docker compose exec dbt dbt seed --target shop --select shop
    ```

4.  **Run dbt**:
    Compile and run the dbt models.
    ```bash
    docker compose exec dbt dbt deps
    docker compose exec dbt dbt debug
    docker compose exec dbt dbt run
    ```

5.  **View Docs**:
    The dbt documentation is automatically served at [http://localhost:8081](http://localhost:8081).
    To update the docs after running models:
    ```bash
    docker compose exec dbt dbt docs generate
    ```
    Then refresh your browser.

## Data Scenario

*   **Source 1 (Postgres)**: `shop.public.customers`, `shop.public.products`.
*   **Source 2 (Iceberg)**: `iceberg.data.events`.
*   **Target (Trino View)**: `dbt_playground.marts.customer_activity`.
