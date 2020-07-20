import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from cognite.client import CogniteClient

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

load_dotenv()
c = CogniteClient()
assert c.login.status().logged_in is True

EXECUTION_DATE = datetime(2020, 6, 20)
NEXT_EXECUTION_DATE = datetime(2020, 6, 21)


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


def get_sensor_data(execution_date, next_execution_date, **context):
    """Query sensor datapoints for the given date.
    Args:
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
    df.reset_index(inplace=true)
    import ipdb;ipdb.set_trace()
    return df


if __name__ == '__main__':
    data = get_sensor_data(EXECUTION_DATE, NEXT_EXECUTION_DATE)
    print(data.head())

