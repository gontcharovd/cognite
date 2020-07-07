import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime
from dotenv import load_dotenv
from cognite.client import CogniteClient

load_dotenv()
c = CogniteClient()
c.login.status()

COMPRESSOR_ID = 7372310232665628
subtree_df = c.assets.retrieve(id=COMPRESSOR_ID).subtree().to_pandas()

sensor_list = [
    '23-PT-92531', \
    '23-PT-92532', \
    '23-PT-92535', \
    '23-PT-92536', \
    '23-PT-92537', \
    '23-PT-92539', \
    '23-PT-92540' 
]
 
pressure_sensors = subtree_df.loc[
    subtree_df['name'].isin(sensor_list),
    ['name', 'id']
]


def get_sensor_data(sensor_id, date):
    """Query sensor datapoints for the given date.
    Args:
        sensor_id (int): unique id of the sensor
        date (date): date for which data is queried
    Returns:
        pd.Series with pressure data per minute
    """
    sensor = c.assets.retrieve(id=sensor_id)
    series = sensor.time_series() 
    series_id = int(series.to_pandas().id.values)
    start = datetime.combine(date, datetime.min.time())
    end = datetime.combine(date, datetime.max.time())
    pressure = c.datapoints.retrieve(
        id=series_id,
        start=start,
        end=end,
        granularity='60s',
        aggregates=['average']
    ).to_pandas()
    return pressure


sensor = '23-PT-92531' 
sensor_id = 5231415482805125 
data = get_sensor_data(
    sensor_id,
    date(2020, 5, 18)
)

plot = data.plot()
plt.show()
