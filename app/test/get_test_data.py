from dotenv import load_dotenv
from cognite.client import CogniteClient
from datetime import datetime

load_dotenv()
c = CogniteClient()
assert c.login.status().logged_in is True

COMPRESSOR_ID = 7372310232665628
SENSOR_NAMES = ['23-PT-92532']
# this timestamp is in UTC
START = datetime(2020, 7, 12, 14, 0, 0, 0) 
END = datetime(2020, 7, 12, 14, 10, 0, 0) 


def get_pt_sensors(compressor_id=COMPRESSOR_ID, sensor_names=SENSOR_NAMES):
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


if __name__ == '__main__':
    sensor_data = get_pt_sensors()
    sensor_id = int(sensor_data.id.values) 
    sensor = c.assets.retrieve(id=sensor_id) 
    time_series_id = sensor.time_series()[0].id
    df = c.datapoints.retrieve_dataframe(
        id=time_series_id,
        start=START,
        end=END,
        granularity='1m',
        aggregates=['average']
    )
    df.reset_index(drop=False, inplace=True)
    df.to_csv('app/test/data.csv', index=False)
    print(df)
