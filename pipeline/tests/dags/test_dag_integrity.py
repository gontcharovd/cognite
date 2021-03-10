import glob
import importlib.util
import os
import pytest
import sys

from airflow.models import DAG

sys.path.append('airflow/plugins/')

DAG_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..', 'airflow', 'dags/**/*.py')
DAG_FILES = glob.glob(DAG_PATH, recursive=True)


@pytest.mark.parametrize('dag_file', DAG_FILES)
def test_dag_integrity(dag_file):
    """Verifies the DAG integrity.

    Specifically, test whether all DAGs:
        1) have have no `end_date`
        2) have <= 32 max active runs
    """
    module_name, _ = os.path.splitext(dag_file)
    module_path = os.path.join(DAG_PATH, dag_file)
    mod_spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(module)

    dag_objects = [v for v in vars(module).values() if isinstance(v, DAG)]

    assert dag_objects

    for dag in dag_objects:
        assert dag.end_date is None
        assert dag.max_active_runs <= 32
