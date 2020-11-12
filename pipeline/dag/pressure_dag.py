"""Apache Airflow Data Pipeline.

Query data through the Cognite Python SDK and write to a PostgreSQL database
"""

import os
import pandas as pd

from custom_airflow.operators import CogniteFetchSensorDataOperator
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv

OUTPUT_DIR='/tmp'
OUTPUT_FILE='postgres_query.sql'

dag = DAG(
    'custom_compressor_pressure',
    start_date=datetime(2020, 10, 1),
    schedule_interval='@daily',
    template_searchpath=OUTPUT_DIR,
    max_active_runs=1,
    concurrency=1
)

fetch_sensor_data = CogniteFetchSensorDataOperator(
    task_id='fetch_sensor_data',
    start_date='{{ ds }}',
    end_date='{{ next_ds }}',
    date_offset=7,
    output_path=os.path.join(OUTPUT_DIR, OUTPUT_FILE),
    dag=dag
)

write_to_postgres = PostgresOperator(
    task_id='write_to_postgres',
    postgres_conn_id='cognite',
    sql=OUTPUT_FILE,
    dag=dag
)

delete_old_records = PostgresOperator(
    task_id='delete_old_records',
    postgres_conn_id='cognite',
    sql="DELETE FROM compressor_pressure \
         WHERE timestamp < DATE(CURRENT_DATE - INTERVAL '90 DAYS');",
    dag=dag
)

recover_disk_space = PostgresOperator(
    task_id='recover_disk_space',
    postgres_conn_id='cognite',
    sql='VACUUM (VERBOSE, ANALYZE) compressor_pressure;',
    # autocommit because VACUUM can't run inside a transaction block
    autocommit=True,
    dag=dag
)

fetch_sensor_data >> write_to_postgres >> delete_old_records >> recover_disk_space
