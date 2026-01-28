from dagster import ScheduleDefinition, define_asset_job

from .assets import data_playground_dbt_assets

# Define a job that materializes all the dbt assets
run_dbt_job = define_asset_job(
    name="run_dbt_job",
    selection=[data_playground_dbt_assets],
)

# Schedule the job to run every 10 minutes
every_10_min_schedule = ScheduleDefinition(
    job=run_dbt_job,
    cron_schedule="*/10 * * * *",
)
