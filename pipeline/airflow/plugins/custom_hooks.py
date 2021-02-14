import os
import pandas as pd

from airflow.hooks.base_hook import BaseHook
from cognite.client import CogniteClient


class CogniteSensorHook(BaseHook):
    """Hook to query sensor data from the Cognite API.

    Abstracts details of the Cognite API and provides several convenience
    methods for fetching sensor data (e.g. get timeseries, sensors, data).
    Also provides support for authentication, etc.
    """

    COMPRESSOR_ID = 7372310232665628
    SENSOR_NAMES = [
        '23-PT-92531',
        '23-PT-92532',
        '23-PT-92535',
        '23-PT-92536',
        '23-PT-92537',
        '23-PT-92539',
        '23-PT-92540'
    ]

    def __init__(self):
        super().__init__()
        self._client = None

    def _authenticate(self):
        "Authenticate and instantiate the Cognite client. """
        if self._client is None:
            api_key = os.environ.get('COGNITE_API_KEY')
            client_name = os.environ.get('COGNITE_CLIENT_NAME')
            api_key = os.environ.get('COGNITE_PROJECT')
            for env_var in [
                'COGNITE_API_KEY',
                'COGNITE_CLIENT_NAME',
                'COGNITE_PROJECT'
            ]:
                if not os.environ.get(env_var):
                    raise ValueError(f'Missing environment variable {env_var}.')

            self._client = CogniteClient(disable_pypi_version_check=True)

    def _get_ts_id(self, sensor_id):
        """Get the id of a timeseries of a given sensor. """
        sensor = self._client.assets.retrieve(id=sensor_id)
        time_series = sensor.time_series()[0]
        time_series_id = time_series.id
        assert isinstance(time_series_id, int)
        return time_series_id

    def _get_sensor_info(self):
        """Get the time series info of chosen sensors.  """
        subtree_df = (
            self._client.assets
            .retrieve(id=self.COMPRESSOR_ID)
            .subtree()
            .to_pandas()
        )
        sensor_info = subtree_df.loc[
            subtree_df['name'].isin(self.SENSOR_NAMES),
            ['name', 'id']
        ]
        sensor_info['ts_id'] = [
            self._get_ts_id(sensor_id) for sensor_id in sensor_info.id
        ]
        return sensor_info

    def get_sensor_data(self, start_date, end_date):
        """Query a range of sensor data and writo to .sql file.

        Args:
            start_date (datetime): sensor data left bound
            end_date (datetime): sensor data right bound
        Returns:
            (pd.DataFrame): timestamp, id, name and pressure
        """
        self._authenticate()
        sensor_info = self._get_sensor_info()

        sensor_df = self._client.datapoints.retrieve_dataframe(
            id=sensor_info.ts_id.values.tolist(),
            start=start_date,
            end=end_date,
            granularity='1m',
            aggregates=['average'],
            include_aggregate_name=False
        )
        sensor_df.index.set_names(['timestamp'], inplace=True)
        sensor_df.reset_index(inplace=True)

        long_df = pd.melt(
            sensor_df,
            id_vars='timestamp',
            var_name='ts_id',
            value_name='pressure'
        ).astype({'ts_id': 'int64'})
        long_df = long_df.join(
            sensor_info.set_index('ts_id')[['name', 'id']],
            on='ts_id'
        )
        long_df.dropna(inplace=True)

        return long_df
