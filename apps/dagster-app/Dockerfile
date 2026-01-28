FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory to the root of the repo (mirrored structure)
WORKDIR /opt/data-playground

# Install dependencies directly to leverage cache
# mirroring the deps in pyproject.toml
RUN pip install \
    dagster \
    dagster-cloud \
    dagster-webserver \
    dagster-dbt \
    dbt-trino \
    dbt-postgres \
    pandas

# Set environment variables
ENV DAGSTER_HOME=/opt/dagster/dagster_home
ENV PYTHONPATH=/opt/data-playground/apps/dagster-app

# Create Dagster home
RUN mkdir -p $DAGSTER_HOME

# Set working directory to the dagster app
WORKDIR /opt/data-playground/apps/dagster-app

# Default command to run Dagster UI
CMD ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000", "-m", "dagster_app"]
