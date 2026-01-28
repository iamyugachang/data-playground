from pathlib import Path
from dagster_dbt import DbtProject

# Absolute path to the root of the repository
# Assuming this file is in apps/dagster-app/dagster_app/project.py
# So repo root is ../../../
REPO_ROOT = Path(__file__).parent.parent.parent.parent.absolute()

DBT_PROJECT_DIR = REPO_ROOT / "apps" / "dbt-analytics"

dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
)
