from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.providers.standard.operators.bash import BashOperator
 
# --- EDIT THESE TWO PATHS to match your machine ---
PROJECT_ROOT = "/Users/arua/Desktop/celo-data-platform"
DBT_DIR      = f"{PROJECT_ROOT}/celo_dbt"
 
# Default settings applied to every task in the DAG
default_args = {
   "owner": "chidi",
   "retries": 3,                          # retry a failed task up to 3 times
   "retry_delay": timedelta(minutes=2),   # wait 2 min, doubling each retry
   "retry_exponential_backoff": True,
   "max_retry_delay": timedelta(minutes=15),
}
 
@dag(
   dag_id="celo_usdm_pipeline",
   description="Extract Celo USDm transfers, then run + test dbt models",
   default_args=default_args,
   schedule="@hourly",                     # run once per day
   start_date=datetime(2026, 1, 1),
   catchup=False,                         # don't backfill history automatically
   max_active_runs=1,                     # never run two copies at once
   tags=["celo", "dbt", "elt"],
)
def celo_usdm_pipeline():
 
   # 1) Extract fresh cUSD transfers via the Forno RPC (Project 1 script)
   extract = BashOperator(
       task_id="extract_usdm",
       bash_command=(
           f'export PATH="/opt/homebrew/bin:$PATH" && '
           f"cd {PROJECT_ROOT}/extractor && "
           f"PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python extract_usdm.py 2000"
        ),
   )
 
   # 2) Build the dbt models (staging -> intermediate -> marts)
   dbt_run = BashOperator(
       task_id="dbt_run",
       bash_command=(
          f'export PATH="/opt/homebrew/bin:$PATH" && '
          f"cd {DBT_DIR} && PIPENV_IGNORE_VIRTUALENVS=1 pipenv run dbt run"
        ),
   )
 
   # 3) Test the models (schema + custom data tests)
   dbt_test = BashOperator(
       task_id="dbt_test",
       bash_command=(
          f'export PATH="/opt/homebrew/bin:$PATH" && '
          f"cd {DBT_DIR} && PIPENV_IGNORE_VIRTUALENVS=1 pipenv run dbt test"
       ),
   )
 
   # Dependency chain: extract must finish before dbt run, etc.
   extract >> dbt_run >> dbt_test
 
celo_usdm_pipeline()