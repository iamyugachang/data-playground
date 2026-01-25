FROM python:3.10-slim

WORKDIR /usr/app

# Install git and other dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dbt-trino and requests (for init script)
RUN pip install dbt-core dbt-trino requests boto3

# We will mount the project here
WORKDIR /usr/app/dbt_project
