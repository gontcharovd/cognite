import os

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from cognite_airflow.hooks import CogniteSensorHook
from datetime import datetime, timedelta


class CogniteFetchSensorDataOperator(BaseOperator):
    """Operator that fetches sensor data from the Cognite API.

    Cognite releases the data with a one week delay. The argument date_offset
    allows to take this delay into account, relative to the execution date.

    Args:
        output_path (str): file where the sensor data will be saved as SQL
        start_date (str templated): sensor data left bound
        end_date (str, templated): sensor data right bound
        date_offset (int): negative timedelta applied to both bounds
    """

    template_fields = ('_start_date', '_end_date')

    @apply_defaults
    def __init__(
        self,
        output_path,
        start_date,
        end_date,
        date_offset,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._output_path = output_path
        self._start_date = start_date
        self._end_date = end_date
        self._date_offset = date_offset

    def execute(self, context):
        hook = CogniteSensorHook()

        start_date = datetime.fromisoformat(self._start_date)
        end_date = datetime.fromisoformat(self._end_date)
        start_date_offset = start_date - timedelta(days=self._date_offset)
        end_date_offset = end_date - timedelta(days=self._date_offset)

        self.log.info(
            f'Fetching sensor data for {start_date} to {end_date}.'
        )
        sensor_data = hook.get_sensor_data(
            start_date=start_date_offset,
            end_date=end_date_offset
        )
        self.log.info(f'Fetched {len(sensor_data)} records.')

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
