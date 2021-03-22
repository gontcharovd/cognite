"""Tests the CogniteSensorOperator

The test initializes an SQLite Airflow metastore that is deleted after the test
"""

import os

from custom_operators.cognite_sensor_operator import CogniteSensorOperator
from init_metastore import init_metastore
from pathlib import Path
from sqlalchemy.orm.exc import NoResultFound


def test_cognite_sensor_operator(
    mocker,
    monkeypatch,
    test_dag,
    tmp_path: Path
):
    """Test the CogniteSensorOperator. """
    metastore_path = os.path.join(os.path.dirname(__file__), 'airflow.db')
    uri = init_metastore(metastore_path)
    monkeypatch.setenv('AIRFLOW__CORE__SQL_ALCHEMY_CONN', uri)
    print(os.environ.get('AIRFLOW__CORE__SQL_ALCHEMY_CONN'))

    task = CogniteSensorOperator(
        task_id='fetch_sensor_data',
        start_date='{{ ds }}',
        end_date='{{ next_ds }}',
        date_offset=7,
        sql_file=tmp_path / 'sensor_data_{{ ds }}.sql',
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
        # os.remove(metastore_path)
