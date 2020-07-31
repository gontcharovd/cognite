"""
Module documentation.
"""

from datetime import datetime
from cognite.client import CogniteClient
from dotenv import load_dotenv

COMPRESSOR_ID = 7372310232665628
SENSOR_NAMES = ['23-PT-92532']
""" this timestamp is in UTC."""
START = datetime(2020, 7, 12, 8, 30, 0, 0)
END = datetime(2020, 7, 12, 20, 10, 0, 0)


def instantiate_cognite_client():
    load_dotenv()
    client = CogniteClient()
    assert client.login.status().logged_in is True
    return client


def get_pt_sensors(client, sensor_names, compressor_id=COMPRESSOR_ID):
    """Get the ids of the chosen compressor sensors.
    Args:
        compressor_id (int): the asset id of the compressor
        sensor_names (list): the names of the pressure sensors
    Returns:
        (pd.DataFrame): name and corresponding id of pressure sensors
    """
    subtree_df = client.assets.retrieve(id=compressor_id).subtree().to_pandas()
    pt_sensors = subtree_df.loc[
        subtree_df['name'].isin(sensor_names),
        ['name', 'id']
    ]
    return pt_sensors


def main():
    client = instantiate_cognite_client()
    sensor_data = get_pt_sensors(client, SENSOR_NAMES)
    sensor_id = int(sensor_data.id.values)
    sensor = client.assets.retrieve(id=sensor_id)
    time_series_id = sensor.time_series()[0].id
    sensor_df = client.datapoints.retrieve_dataframe(
        id=time_series_id,
        start=START,
        end=END,
        granularity='1m',
        aggregates=['average']
    )
    sensor_df.reset_index(drop=False, inplace=True)
    sensor_df.to_csv('app/test/data.csv', index=False)
    print(sensor_df)


if __name__ == '__main__':
    main()
