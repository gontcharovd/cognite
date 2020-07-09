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


def get_pt_sensors(compressor_id=COMPRESSOR_ID, sensor_names=SENSOR_NAMES):
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
    return pt_sensors


def get_sensor_data(sensors, date):
    """Query sensor datapoints for the given date.
    Args:
        sensors (pd.DataFrame): sensor names and ids
        date (date): data for which to query data 
    Returns:
        (pd.DataFrame): average pressure data per minute
    """
    start = datetime.combine(date, datetime.min.time())
    end = datetime.combine(date, datetime.max.time())
    pt_sensors = c.assets.retrieve_multiple(ids=pt_ids)
    sensors['series_ids'] = [serie.id for serie in pt_sensors.time_series()]
    df = c.datapoints.retrieve_dataframe(
        id=list(sensors.series_ids),
        start=start,
        end=end,
        granularity='1h',
        aggregates=['average']
    )
    # column names should be sensor ids
    names = list(df.columns.values)
    df.columns = [n.split('|')[0] for n in names]
    # save data in long format
    df.index.set_names(['timestamp'], inplace=True)
    df.reset_index(inplace=True)
    long_df = pd.melt(
        df,
        id_vars='timestamp',
        var_name='series_id',
        value_name='pressure'
    ).astype({'series_id': 'int64'})
    # long_df = long_df.join(sensors.set_index('id'), on='id')
    return long_df


pt_sensors = get_pt_sensors()
pt_ids = list(pt_sensors.id.values)
data = get_sensor_data(
    pt_sensors,
    date(2020, 5, 18)
)

plot = data.plot()
plt.show()
