from google.cloud import bigquery
from config import PROJECT_ID, RAW_DATASET, BQ_LOCATION
 
_client = bigquery.Client(project=PROJECT_ID, location=BQ_LOCATION)
 
def load_dataframe(df, table_name: str, write_mode: str = "WRITE_TRUNCATE"):
   table_id = f"{PROJECT_ID}.{RAW_DATASET}.{table_name}"
   job_config = bigquery.LoadJobConfig(
       write_disposition=write_mode,        # TRUNCATE = replace, APPEND = add
       autodetect=True,                     # infer schema from the DataFrame
   )
   job = _client.load_table_from_dataframe(df, table_id, job_config=job_config)
   job.result()                             # block until finished
   n = _client.get_table(table_id).num_rows
   print(f"Loaded {len(df):,} rows -> {table_id} (table now {n:,} rows)")
   return table_id