"""Contains pytest fixtures used in the Airflow operator unit tests. """

import datetime
import os
import pytest

from airflow.models import DAG
from pytest_docker_tools import container, fetch, network

START_DATE = datetime.datetime(2021, 1, 1)
DB_INIT_SCRIPT = os.path.join(
    os.path.dirname(__file__),
    '..', '..', '..', '..',
    'database', 'db-init.sh'
)


@pytest.fixture
def test_dag():
    """Defines an Airflow dag that can be used by Airflow tasks. """
    args = {'owner': 'airflow', 'start_date': START_DATE}
    return DAG('test_dag', default_args=args, schedule_interval='@daily')


# networks are necessary to extract the
# random IP-Adress of the containers
container_network = network()

"""postgres container with automated initialization of tables and data. """
postgres_image = fetch(repository='postgres:13')
postgres_container = container(
    image='{postgres_image.id}',
    scope='function',
    ports={'5432/tcp': None},
    environment={'POSTGRES_PASSWORD': 'test'},
    volumes={
        DB_INIT_SCRIPT: {'bind': '/docker-entrypoint-initdb.d/init-db.sh'}
    },
    network='{container_network.name}'
)
