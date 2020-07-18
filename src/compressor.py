# What is the typical difference between the input and output pressure of the compressor?

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from cognite.client import CogniteClient

load_dotenv()
c = CogniteClient()
c.login.status()

COMPRESSOR_ID = 7372310232665628

subtree = c.assets.retrieve(id=COMPRESSOR_ID).subtree()
subtree_df = subtree.to_pandas()

events = subtree.events()
events_df = events.to_pandas()
events_df.type.value_counts()

work_df = events_df[events_df.type.str.contains('Work')]
pressure_sensors = subtree_df[subtree_df.name.str.contains('PT')]

sensor_list = [
    '23-PT-92531'
    '23-PT-92532'
    '23-PT-92535'
    '23-PT-92536'
    '23-PT-92537'
    '23-PT-92539'
    '23-PT-92540'
]

# get daily data for all these sensors
id_sensor_before = pressure_sensors.loc[
    pressure_sensors.name=='23-PT-92532',
    'id'
].values
id_sensor_after = pressure_sensors.loc[
    pressure_sensors.name=='23-PT-92539',
    'id'
].values

id_sensor_before = int(id_sensor_before)
id_sensor_after = int(id_sensor_after)

sensor_before = c.assets.retrieve(id=id_sensor_before)
sensor_after = c.assets.retrieve(id=id_sensor_after)

pressure_series_before = sensor_before.time_series()
pressure_series_after = sensor_after.time_series()

pressure_series_before.plot(
    start='30d-ago',
    end='now',
    granularity='1d',
    aggregates=['average']
)

pressure_series_after.plot(
    start='30d-ago',
    end='now',
    granularity='1d',
    aggregates=['average']
)

pressure_before = c.datapoints.retrieve(
    id=int(pressure_series_before.to_pandas().id.values),
    start='10d-ago',
    end='now',
    granularity='1m',
    aggregates=['average']
).to_pandas()

pressure_before.rename('p_before', inplace=True)

pressure_after = c.datapoints.retrieve(
    id=int(pressure_series_after.to_pandas().id.values),
    start='30d-ago',
    end='now',
    granularity='1d',
    aggregates=['average']
).to_pandas()

pressure_df = pd.concat([pressure_before, pressure_after], axis=1)
pressure_df.columns = ['p_before', 'p_after']
pressure_df['p_diff'] = pressure_df['p_after'] - pressure_df['p_before'] 

plot = pressure_df['p_diff'].plot()
plt.plot(pressure_df)
plt.show()
