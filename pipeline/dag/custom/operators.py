import os

from airflow.models import BaseOperator
from airflow.utils import apply_defaults

from custom.hooks import CogniteHook

class CogniteOperator(BaseOperator):
    """Operator that fetches sensor data from the Cognite API.

    Args:
        output_path (str): file where the sensor data will be saved as SQL
        start_date (datetime, templated): sensor data left bound
        end_date (datetime, templated): sensor data right bound
        date_offset (int): negative timedelta applied to both bounds
    """

    @apply_defaults
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self._output_path = output_path
        self._start_date = start_date
        self._end_date = end_date

    def execute(self, context):
        hook = CogniteHook()



#         with open(SQL_PATH, 'w') as handle:
#             for _, vals in long_df.iterrows():
#                 handle.write(
#                     'INSERT INTO compressor_pressure VALUES ('
#                     f"'{vals['timestamp']}Z', "
#                     f"{vals['id']}, "
#                     f"'{vals['name']}', "
#                     f"{vals['pressure']}) "
#                     "ON CONFLICT DO NOTHING;\n"
#                 )
