from airflow.hooks.base_hook import BaseHook
from cognite.client import CogniteClient


class CogniteHook(BaseHook):
    """Hook for the Cognite API.

    Abstracts details of the Cognite API and provides several convenience
    methods for fetching sensor data (e.g. get timeseries, sensors, data).
    Also provides support for authentication, etc.

    Args:
        api_key (str): the Cognite API key
        client_name (str): name of the cognite client
        project (str): the name of the Open Industrial Data Project
    """

    COMPRESSOR_ID = 7372310232665628
    SQL_PATH = '/tmp/postgres_query.sql'
    SENSOR_NAMES = [
        '23-PT-92531',
        '23-PT-92532',
        '23-PT-92535',
        '23-PT-92536',
        '23-PT-92537',
        '23-PT-92539',
        '23-PT-92540'
    ]

    def __init__(self, client_name='cognite', project='publicdata'):
        super().__init__(source=None)
        self._client = None
        self._api_key = os.environ.get('COGNITE_API_KEY')
        self._client_name = client_name
        self._project = project

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Closes any active session. """
        if self.session:
            self.session.close()
        self._client = None

    def _get_client(self):
        "Authenticate and return the Cognite client. """
        if self._client is None:
            if not self._api_key:
                raise ValueError('No Cognite api_key specified.')

            self._client = CogniteClient(
                api_key=self._api_key,
                client_name=self._client_name,
                project=self._project
            )
        return self._client

    def _get_ts_id(client, sensor_id):
        """Get the id of a timeseries of a given sensor.

        Args:
            client: Cognite SDK client
            sennsor_id (int): asset id of a sensor
        Returns:
            (int): time series id of a sensor's time series
        """
        sensor = client.assets.retrieve(id=sensor_id)
        time_series = sensor.time_series()[0]
        time_series_id = time_series.id
        assert isinstance(time_series_id, int)
        return time_series_id

    def _get_sensor_info(client, sensor_names=SENSOR_NAMES):
        """Get the properties of chosen compressor sensors.

        Args:
            client: Cognite SDK client
            sensor_names (list): pressure sensors names
        Returns:
            (pd.DataFrame): name, sensor id and time series id of sensors
        """
        subtree_df = (
            client.assets
            .retrieve(id=COMPRESSOR_ID)
            .subtree()
            .to_pandas()
        )
        sensor_info = subtree_df.loc[
            subtree_df['name'].isin(sensor_names),
            ['name', 'id']
        ]
        sensor_info['ts_id'] = [
            _get_ts_id(client, s_id) for s_id in sensor_info.id
        ]
        return sensor_info

    def get_sensor_data(self, start_date, end_date, date_offset=8):
        """Query a range of sensor data and writo to .sql file.

        Args:
            start_date (datetime): sensor data left bound
            end_date (datetime): sensor data right bound
            date_offset (int): negative timedelta applied to both bounds
        """
        start = start_date - timedelta(days=date_offset)
        end = end_date - timedelta(days=date_offset)
        client = self._get_client()

        sensor_info = self._get_sensor_info(client)

        sensor_df = client.datapoints.retrieve_dataframe(
            id=sensor_info.ts_id.values.tolist(),
            start=start,
            end=end,
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

        with open(SQL_PATH, 'w') as handle:
            for _, vals in long_df.iterrows():
                handle.write(
                    'INSERT INTO compressor_pressure VALUES ('
                    f"'{vals['timestamp']}Z', "
                    f"{vals['id']}, "
                    f"'{vals['name']}', "
                    f"{vals['pressure']}) "
                    "ON CONFLICT DO NOTHING;\n"
                )
