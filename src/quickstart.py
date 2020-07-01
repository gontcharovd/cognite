import os
import pandas as pd
from cognite.client import CogniteClient
from cognite.client.data_classes import Asset
from cognite.client.exceptions import CogniteAPIError

os.environ['COGNITE_API_KEY'] = 'MmM5NGUxYzQtOGE1Ny00ZDJkLWEzYTItMGQ4ZjM0NTFkZTAw' 
os.environ['COGNITE_CLIENT_NAME'] = 'Denis' 

c = CogniteClient()
status = c.login.status()

ts_list = c.time_series.list(include_metadata=False)

my_time_series = c.time_series.retrieve(id=6190956317771)
my_time_series.plot()

my_datapoints = c.datapoints.retrieve(
    id=6190956317771,
    start="100d-ago",
    end="now",
    aggregates=["max"],
    granularity="48h"
)
my_datapoints.plot()

datapoints_df = my_datapoints.to_pandas()
datapoints_df.head()

root = Asset(name="root", external_id="1")
child = Asset(name="child", external_id="2", parent_external_id="1")
descendant = Asset(name="descendant", external_id="3", parent_external_id="2")

c.assets.create_hierarchy([root, child, descendant])

try:
    c.assets.create_hierarchy([root, child, descendant])
except CogniteAPIError as e:
    assets_posted = e.successful
    assets_may_have_been_posted = e.unknown
    assets_not_posted = e.failed

print(assets_posted) 
print(assets_may_have_been_posted) 
print(assets_not_posted) 
