import sys

sys.path.append('custom_airflow')
from hooks import CogniteHook
from datetime import datetime

start_date = datetime(2020, 10, 10, 0, 0, 0)
end_date = datetime(2020, 10, 10, 0, 10, 0)

hook = CogniteHook()

sensor_data = hook.get_sensor_data(start_date, end_date)

print(sensor_data)
