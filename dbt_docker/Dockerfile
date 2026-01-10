FROM python:3.10-slim

WORKDIR /usr/app

# Install git and other dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dbt-trino
RUN pip install dbt-core dbt-trino

# We will mount the project here
WORKDIR /usr/app/dbt_project
