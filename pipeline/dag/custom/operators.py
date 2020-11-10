import os

from airflow.models import BaseOperator
from airflow.utils import apply_defaults
from custom.hooks import CogniteHook
from datetime import datetime, timedelta

class CogniteFetchSensorDataOperator(BaseOperator):
    """Operator that fetches sensor data from the Cognite API.

    Args:
        output_path (str): file where the sensor data will be saved as SQL
        start_date (datetime, templated): sensor data left bound
        end_date (datetime, templated): sensor data right bound
        date_offset (int): negative timedelta applied to both bounds
    """

    template_fields = ('_start_date', '_end_date', '_output_path')

    @apply_defaults
    def __init__(
        self,
        output_path,
        start_date='{{ ds }}',
        end_date='{{ next_ds }}',
        date_offset=8,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._output_path = output_path
        self._start_date = start_date
        self._end_date = end_date
        self._date_offset = date_offset

    def execute(self, context):
        hook = CogniteHook()

        # start_date = datetime(self._start_date) - timedelta(days=self._date_offset)
        # end_date = datetime(self._end_date) - timedelta(days=self._date_offset)

        start_date = self._start_date
        end_date = self._end_date

        self.log.info(
            f'Fetching sensor data for {start_date} to {end_date}'
        )
        sensor_data = hook.get_sensor_data(
            start_date=start_date,
            end_date=end_date
        )
        self.log.info(f'Fetched {len(sensor_data)} ratings')

        # make sure the output directory exists
        output_dir = os.path.dirname(self._output_path)
        os.makedirs(output_dir, exist_ok=True)

        with open(self._output_path, 'w') as handle_:
            for _, vals in sensor_data.iterrows():
                handle_.write(
                    'INSERT INTO compressor_pressure VALUES ('
                    f"'{vals['timestamp']}Z', "
                    f"{vals['id']}, "
                    f"'{vals['name']}', "
                    f"{vals['pressure']}) "
                    "ON CONFLICT DO NOTHING;\n"
                )
