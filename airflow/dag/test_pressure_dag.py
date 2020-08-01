"""Unit test of the data pipeline. """

import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from cognite.client import CogniteClient

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
OUTPUT_PATH = os.path.join(
    '/',
    'home',
    'gontcharovd',
    'code',
    'personal_projects',
    'cognite',
    'tmp'
)
OUTPUT_FILE = 'postgres_query.sql'

" maybe add a wrapper around _get_sensor_data to make it return data

def main():
    output_path = os.path.join(OUTPUT_PATH, OUTPUT_FILE)
    start = datetime(2020, 7, 12, 5, 0, 0, 0)
    end = datetime(2020, 7, 12, 10, 0, 0, 0)
    client = _get_cognite_client()
    data = _get_sensor_data(client, output_path, start, end)
    print(data.head())


"""23-PT-92532 CET
2020-07-04_07:00:00 2.43953538633042
"""

"""23-PT-92537 CET
2020-07-17_12:02:00 0.438095241785049
"""


if __name__ == '__main__':
    main()
