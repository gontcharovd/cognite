import os
import pandas as pd
import numpy as np
from cognite.client import CogniteClient
from cognite.client.data_classes import Asset
from cognite.client.exceptions import CogniteAPIError

os.environ['COGNITE_API_KEY'] = 'MmM5NGUxYzQtOGE1Ny00ZDJkLWEzYTItMGQ4ZjM0NTFkZTAw' 
os.environ['COGNITE_CLIENT_NAME'] = 'Denis' 
os.environ['COGNITE_PROJECT'] = 'publicdata' 

np.arange(10)

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

my_asset = Asset(name="my first asset", parent_id=123)
c.assets.create(my_asset)
print(my_asset)

root = Asset(name="root", external_id="1")
child = Asset(name="child", external_id="2", parent_external_id="1")
descendant = Asset(name="descendant", external_id="3", parent_external_id="2")
c.assets.create_hierarchy([root, child, descendant])

try:
    c.assets.create_hierarchy([root, child, descendant])
    print('success!')
except CogniteAPIError as e:
    assets_posted = e.successful
    assets_may_have_been_posted = e.unknown
    assets_not_posted = e.failed

print(assets_posted) 
print(assets_may_have_been_posted) 
print(assets_not_posted) 

asset_list = c.assets.list(include_metadata=False)

