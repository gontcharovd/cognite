"""Apache Airflow Data Pipeline.

Query data through the Cognite Python SDK and write to an SQL file
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from cognite.client import CogniteClient
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator

COMPRESSOR_ID = 7372310232665628
SENSOR_NAMES = [
    '23-PT-92531',
    '23-PT-92532',
    '23-PT-92535',
    '23-PT-92536',
    '23-PT-92537',
    '23-PT-92539',
    '23-PT-92540'
]
OUTPUT_PATH = os.environ.get('TMP_PATH')
OUTPUT_FILE = 'postgres_query.sql'


dag = DAG(
    'compressor_pressure',
    start_date=datetime(2020, 5, 1),
    schedule_interval='@daily',
    template_searchpath=OUTPUT_PATH,
    max_active_runs=1,
    concurrency=1
)


def _get_cognite_client():
    """Authenticate and return Cognite client. """
    client = CogniteClient()
    assert client.login.status().logged_in is True
    return client


def _get_ts_id(client, sensor_id):
    """Get the id of a timeseries of a given sensor. """
    sensor = client.assets.retrieve(id=sensor_id)
    time_series = sensor.time_series()[0]
    time_series_id = time_series.id
    assert isinstance(time_series_id, int)
    return time_series_id


def _get_sensor_info(client, sensor_names):
    """Get the properties of chosen compressor sensors.
    Args:
        client: Cognite SDK client
        sensor_names: list of pressure sensors names
    Returns:
        (pd.DataFrame): name, sensor id and time series id of sensors
    """
    subtree_df = client.assets.retrieve(id=COMPRESSOR_ID).subtree().to_pandas()
    sensor_info = subtree_df.loc[
        subtree_df['name'].isin(sensor_names),
        ['name', 'id']
    ]
    sensor_info['ts_id'] = [
        _get_ts_id(client, s_id) for s_id in sensor_info.id
    ]
    return sensor_info


def _get_sensor_data(client, output_path, execution_date,
                     next_execution_date, **context):
    """Query sensor data and writo to .sql file.
    Args:
        client: Cognite SDK client
        output_path (str): file where the postgres SQL query will be written
        execution_date (datetime): Airflow execution date
        next_execution_date (datetime): Airflow next execution date
    """
    # data is released with a delay of one week
    start = execution_date - timedelta(days=8)
    end = next_execution_date - timedelta(days=8)
    sensor_info = _get_sensor_info(client, SENSOR_NAMES)
    sensor_df = client.datapoints.retrieve_dataframe(
        id=sensor_info.ts_id.values.tolist(),
        start=start,
        end=end,
        granularity='1m',
        aggregates=['average'],
        include_aggregate_name=False
    )
    sensor_df.index.set_names(['timestamp'], inplace=True)
    sensor_df.reset_index(inplace=True)
    long_df = pd.melt(
        sensor_df,
        id_vars='timestamp',
        var_name='ts_id',
        value_name='pressure'
    ).astype({'ts_id': 'int64'})
    long_df = long_df.join(
        sensor_info.set_index('ts_id')[['name', 'id']],
        on='ts_id'
    )
    long_df.dropna(inplace=True)
    with open(output_path, 'w') as handle:
        for _, vals in long_df.iterrows():
            handle.write(
                'INSERT INTO compressor_pressure VALUES ('
                f"'{vals['timestamp']}Z', "
                f"{vals['id']}, "
                f"'{vals['name']}', "
                f"{vals['pressure']}) "
                "ON CONFLICT DO NOTHING;\n"
            )


get_sensor_data = PythonOperator(
    task_id='get_sensor_data',
    python_callable=_get_sensor_data,
    provide_context=True,
    op_kwargs={
        'client': _get_cognite_client(),
        'output_path': os.path.join(OUTPUT_PATH, OUTPUT_FILE)
    },
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
    # autocommit because VACUUM can't run
    # inside a transaction block
    autocommit=True,
    dag=dag
)

get_sensor_data >> write_to_postgres >> delete_old_records >> recover_disk_space
