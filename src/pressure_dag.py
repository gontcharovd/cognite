
import os
import airflow
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from cognite.client import CogniteClient
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator

COMPRESSOR_ID = 7372310232665628
SENSOR_NAMES = [
    '23-PT-92531', \
    '23-PT-92532', \
    '23-PT-92535', \
    '23-PT-92536', \
    '23-PT-92537', \
    '23-PT-92539', \
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

load_dotenv()
c = CogniteClient()
assert c.login.status().logged_in is True

# today = 2020-07-18
# data available partly for today - 7 days
# first complete data day: 2020-07-10
# therefore:
    # start = ds - 8
    # end = ds_next - 8

dag = DAG(
    'pressure',
    start_date=airflow.utils.dates.days_ago(10),
    schedule_interval='@daily',
    template_searchpath=OUTPUT_PATH
)


def _get_pt_sensors(compressor_id=COMPRESSOR_ID, sensor_names=SENSOR_NAMES):
    """Get the ids of the chosen compressor sensors.
    Args:
        compressor_id (int): the asset id of the compressor
        sensor_names (list): the names of the pressure sensors
    Returns:
        (pd.DataFrame): name and corresponding id of pressure sensors 
    """
    subtree_df = c.assets.retrieve(id=COMPRESSOR_ID).subtree().to_pandas()
    pt_sensors = subtree_df.loc[
        subtree_df['name'].isin(SENSOR_NAMES),
        ['name', 'id']
    ]
    return pt_sensors


def _get_sensor_data(output_path, execution_date, next_execution_date, **context):
    """Query sensor datapoints for the given date.
    Args:
        output_path (str): file where the postgres SQL query will be written
        execution_date (datetime): Airflow execution date
        next_execution_date (datetime): Airflow next execution date
    """
    # data is available with a delay of one week
    start = execution_date - timedelta(days=8)
    end = next_execution_date - timedelta(days=8) 
    sensors = _get_pt_sensors()
    pt_ids = list(sensors.id.values)
    pt_sensors = c.assets.retrieve_multiple(ids=pt_ids)
    sensors['series_id'] = [serie.id for serie in pt_sensors.time_series()]
    df = c.datapoints.retrieve_dataframe(
        id=list(sensors.series_id),
        start=start,
        end=end,
        granularity='1m',
        aggregates=['average']
    )
    # column names should be sensor ids
    names = list(df.columns.values)
    df.columns = [n.split('|')[0] for n in names]
    df.index.set_names(['timestamp'], inplace=True)
    df.reset_index(inplace=True)
    long_df = pd.melt(
        df,
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
                'INSERT INTO pressure VALUES ('
                f"'{vals['timestamp']}', "
                f"{vals['id']}, "
                f"'{vals['name']}', "
                f"{vals['pressure']});\n"
            )


get_sensor_data = PythonOperator(
    task_id='get_sensor_data',
    python_callable=_get_sensor_data,
    provide_context=True,
    op_kwargs= {'output_path': os.path.join(OUTPUT_PATH, OUTPUT_FILE)},
    dag=dag
)


write_to_postgres = PostgresOperator(
   task_id='write_to_postgres',
   postgres_conn_id='cognite',
   sql=OUTPUT_FILE,
   dag=dag
)


get_sensor_data >> write_to_postgres 
