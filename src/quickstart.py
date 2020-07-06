import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from cognite.client import CogniteClient
from cognite.client.data_classes import Asset
from cognite.client.exceptions import CogniteAPIError

load_dotenv()

c = CogniteClient()
status = c.login.status()

ts_list = c.time_series.list(include_metadata=False)
print(ts_list)

TS_ID = 6190956317771

my_time_series = c.time_series.retrieve(id=TS_ID)
my_time_series.plot(start='30d-ago', end='now')

my_datapoints = c.datapoints.retrieve(
    id=TS_ID,
    start="100d-ago",
    end="now",
    aggregates=["max"],
    granularity="48h"
)
my_datapoints.plot()

datapoints_df = my_datapoints.to_pandas()
datapoints_df.head()

asset_list = c.assets.list(limit=1)

oil_asset = c.assets.search(name='oil')
asset_df = oil_asset.to_pandas()
oil_asset_id = asset_df['id'].values
oil_asset_id = int(oil_asset_id)

subtree_root_asset=oil_asset_id
subtree = c.assets.retrieve(id=subtree_root_asset).subtree()
related_events = subtree.events()

