"""Tests the CogniteSensorOperator

The test initializes an SQLite Airflow metastore that is deleted after the test
"""

import os
import subprocess

from custom_operators.cognite_sensor_operator import CogniteSensorOperator
from pathlib import Path
from sqlalchemy.orm.exc import NoResultFound


def test_cognite_sensor_operator(
    mocker,
    test_dag,
    tmp_path: Path
):
    """Test the CogniteSensorOperator. """
    metastore_path = os.path.join(os.path.dirname(__file__), 'airflow.db')
    uri = f'sqlite:///{metastore_path}'

    os.environ['AIRFLOW__CORE__SQL_ALCHEMY_CONN'] = uri
    os.environ['AIRFLOW__CORE__LOAD_EXAMPLES'] = 'False'
    os.environ['AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS'] = 'False'

    init_metastore = subprocess.Popen(['airflow', 'db', 'init'])
    init_metastore.wait()
    print('Created Airflow metastore')

    task = CogniteSensorOperator(
        task_id='fetch_sensor_data',
        start_date='{{ ds }}',
        end_date='{{ next_ds }}',
        date_offset=7,
        sql_file='sensor_data_{{ ds }}.sql',
        dag=test_dag
    )

    try:
        print('Running task...')
        task.run(
            start_date=test_dag.default_args['start_date'],
            end_date=test_dag.default_args['start_date']
        )
    except NoResultFound:
        print('Caught expected `sqlalchemy.orm.exc.NoResultFound` exception')
    finally:
        print('Deleted Airflow metastore')
        os.remove(metastore_path)
