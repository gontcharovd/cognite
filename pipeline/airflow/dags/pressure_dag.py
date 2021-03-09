"""Apache Airflow Data Pipeline.

Query data through the Cognite Python SDK and write to a PostgreSQL database
"""

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from custom_operators.cognite_sensor_operator import CogniteSensorOperator
from custom_operators.postgres_file_operator import PostgresFileOperator
from datetime import datetime

dag = DAG(
    'compressor_pressure',
    start_date=datetime(2021, 1, 1),
    end_date=datetime(2021, 2, 1),
    schedule_interval='@daily',
    max_active_runs=8
)

fetch_sensor_data = CogniteSensorOperator(
    task_id='fetch_sensor_data',
    start_date='{{ ds }}',
    end_date='{{ next_ds }}',
    date_offset=7,
    sql_file='tmp/sensor_data_{{ ds }}.sql',
    dag=dag
)

write_new_records = PostgresFileOperator(
    task_id='write_new_records',
    postgres_conn_id='application_db',
    delete=True,
    dag=dag
)

delete_old_records = PostgresOperator(
    task_id='delete_old_records',
    postgres_conn_id='application_db',
    sql="DELETE FROM compressor_pressure \
         WHERE timestamp < DATE(CURRENT_DATE - INTERVAL '90 DAYS');",
    dag=dag
)

recover_space = PostgresOperator(
    task_id='recover_disk_space',
    postgres_conn_id='application_db',
    sql='VACUUM (VERBOSE, ANALYZE) compressor_pressure;',
    # autocommit because VACUUM can't
    # run inside a transaction block
    autocommit=True,
    dag=dag
)

fetch_sensor_data >> write_new_records >> delete_old_records >> recover_space
