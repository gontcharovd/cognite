"""Apache Airflow Data Pipeline.

Query data through the Cognite Python SDK and write to an SQL file.
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
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
OUTPUT_PATH = os.path.join(
    '/',
    'home',
    'gontcharovd',
    'code',
    'personal_projects',
    'cognite',
    'tmp'
)
OUTPUT_FILE = 'postgres_query.sql'


def _get_cognite_client():
    """get_cognite_client at Cognite SDK.
    Returns: 
        Cognite client
    """
    assert os.path.exists('.env')
    load_dotenv()
    client = CogniteClient()
    assert client.login.status().logged_in is True
    return client


def _get_pt_sensors(client, sensor_names, compressor_id=COMPRESSOR_ID):
    """Get the ids of the chosen compressor sensors.
    Args:
        compressor_id (int): the asset id of the compressor
        sensor_names (list): the names of the pressure sensors
    Returns:
        (pd.DataFrame): name and corresponding id of pressure sensors
    """
    subtree_df = client.assets.retrieve(id=compressor_id).subtree().to_pandas()
    pt_sensors = subtree_df.loc[
        subtree_df['name'].isin(sensor_names),
        ['name', 'id']
    ]
    return pt_sensors


def _get_sensor_data(client, output_path, execution_date,
                     next_execution_date, **context):
    """Query sensor datapoints for the given date.
    Args:
        output_path (str): file where the postgres SQL query will be written
        execution_date (datetime): Airflow execution date
        next_execution_date (datetime): Airflow next execution date
    """
    # data is available with a delay of one week
    start = execution_date - timedelta(days=8)
    end = next_execution_date - timedelta(days=8)
    sensor_info = _get_pt_sensors(client, SENSOR_NAMES)
    sensor_ids = list(sensor_info.id.values)
    sensors = client.assets.retrieve_multiple(ids=sensor_ids)
    # the bug is here!! The order of returned sensor assets is not
    # equal to the alphabetical order of the sensor_info
    sensor_info['time_series_id'] = [ts.id for ts in sensors.time_series()]
    sensor_df = client.datapoints.retrieve_dataframe(
        id=list(sensors.time_series_id),
        start=start,
        end=end,
        granularity='1m',
        aggregates=['average']
    )
    # column names should be sensor ids
    names = list(sensor_df.columns.values)
    sensor_df.columns = [n.split('|')[0] for n in names]
    sensor_df.index.set_names(['timestamp'], inplace=True)
    sensor_df.reset_index(inplace=True)
    long_df = pd.melt(
        sensor_df,
        id_vars='timestamp',
        var_name='series_id',
        value_name='pressure'
    ).astype({'series_id': 'int64'})
    long_df = long_df.join(
        sensors.set_index('series_id')[['name', 'id']],
        on='series_id'
    )
    long_df.dropna(inplace=True)
    with open(output_path, 'w') as handle:
        for _, vals in long_df.iterrows():
            handle.write(
                'INSERT INTO compressor_pressure VALUES ('
                f"'{vals['timestamp']}', "
                f"{vals['id']}, "
                f"'{vals['name']}', "
                f"{vals['pressure']}) "
                "ON CONFLICT DO NOTHING;\n"
            )


dag = DAG(
    'compressor_pressure',
    start_date=datetime(2020, 7, 1),
    schedule_interval='@daily',
    template_searchpath=OUTPUT_PATH
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

get_sensor_data >> write_to_postgres
