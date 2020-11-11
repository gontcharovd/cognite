from datetime import datetime
from custom.operators import CogniteFetchSensorDataOperator
from custom.hooks import CogniteHook

hook =CogniteHook()

client = hook._get_client()

operator = CogniteFetchSensorDataOperator(
    output_path='/tmp/query.sql',
    start_date=datetime(2020, 10, 10),
    end_date=datetime(2020, 10, 15),
    date_offset=1
)
