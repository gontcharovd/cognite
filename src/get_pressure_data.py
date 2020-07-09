import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime
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
c.login.status()


def get_sensor_ids(compressor_id=COMPRESSOR_ID, sensor_names=SENSOR_NAMES):
    """Get the ids of the chosen compressor sensors.
    Args:
        sensor_ids (list): list with sensor ids
        date (date): data for which to query data 
    Returns:
        pd.DataFrame with average pressure data per minute
    """
    subtree_df = c.assets.retrieve(id=COMPRESSOR_ID).subtree().to_pandas()
    pt_sensors = subtree_df.loc[
        subtree_df['name'].isin(SENSOR_NAMES),
        ['name', 'id']
    ]
    pt_ids = list(pressure_sensors.id.values)
    return pt_ids


def get_sensor_data(sensor_ids, date):
    """Query sensor datapoints for the given date.
    Args:
        sensor_ids (list): list with sensor ids
        date (date): data for which to query data 
    Returns:
        pd.DataFrame with average pressure data per minute
    """
    start = datetime.combine(date, datetime.min.time())
    end = datetime.combine(date, datetime.max.time())
    pt_sensors = c.assets.retrieve_multiple(ids=pt_ids)
    series_ids = [serie.id for serie in pt_sensors.time_series()]
    pressure_df = c.datapoints.retrieve_dataframe(
        id=series_ids,
        start=start,
        end=end,
        granularity='1h',
        aggregates=['average']
    )
    # column names should be sensor ids
    names = list(pressure_df.columns.values)
    pressure_df.columns = [n.split('|')[0] for n in names]
    return pressure_df


pt_ids = get_sensor_ids()

data = get_sensor_data(
    pt_ids,
    date(2020, 5, 18)
)

plot = data.plot()
plt.show()
