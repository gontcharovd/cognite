import os

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from custom_hooks.cognite_sensor_hook import CogniteSensorHook
from datetime import datetime, timedelta


class CogniteSensorOperator(BaseOperator):
    """Operator that fetches sensor data from the Cognite API.

    Cognite releases the data with a one week delay. The argument date_offset
    allows to take this delay into account, relative to the execution date.

    Args:
        sql_file: (templated) file where the sensor data will be saved as SQL
        start_date: (templated) sensor data left bound
        end_date: (templated) sensor data right bound
        date_offset: negative timedelta applied to both bounds
    """

    template_fields = ('start_date', 'end_date', 'sql_file')

    @apply_defaults
    def __init__(
        self,
        sql_file: str,
        start_date: str,
        end_date: str,
        date_offset: int,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.sql_file = sql_file
        self.start_date = start_date
        self.end_date = end_date
        self.date_offset = date_offset

    def execute(self, context):
        hook = CogniteSensorHook()

        start_date = datetime.fromisoformat(self.start_date)
        end_date = datetime.fromisoformat(self.end_date)
        start_date_offset = start_date - timedelta(days=self.date_offset)
        end_date_offset = end_date - timedelta(days=self.date_offset)

        self.log.info(
            f'Fetching sensor data for {start_date} to {end_date}.'
        )
        sensor_data = hook.get_sensor_data(
            start_date=start_date_offset,
            end_date=end_date_offset
        )
        self.log.info(f'Fetched {len(sensor_data)} records.')

        # make sure the output directory exists
        output_dir = os.path.dirname(self.sql_file)
        os.makedirs(output_dir, exist_ok=True)

        with open(self.sql_file, 'w') as f:
            for _, vals in sensor_data.iterrows():
                f.write(
                    'INSERT INTO compressor_pressure VALUES ('
                    f"'{vals['timestamp']}Z', "
                    f"{vals['id']}, "
                    f"'{vals['name']}', "
                    f"{vals['pressure']}) "
                    "ON CONFLICT DO NOTHING;\n"
                )
