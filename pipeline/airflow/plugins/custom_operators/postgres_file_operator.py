import os

from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults


class PostgresFileOperator(PostgresOperator):
    """Extends the PostgresOperator to read sql from a templated file path.

    The file path is retrieved through XCom and the file is deleted
    if the upload succeeds and `delete` is True.

    Args:
        delete: delete the `sql_file` after successful upload or not
    """

    @apply_defaults
    def __init__(self, delete: bool, **kwargs) -> None:
        super().__init__(sql=None, **kwargs)
        self.delete = delete

    def execute(self, context):
        task_instance = context['task_instance']
        sql_file = task_instance.xcom_pull(
            task_ids='fetch_sensor_data', key='sql_file')
        self.log.info(f'Reading from SQL-file: {sql_file}')
        self.hook = PostgresHook(
            postgres_conn_id=self.postgres_conn_id, schema=self.database)
        with open(sql_file, 'r') as f:
            sql = f.read()
        self.hook.run(sql, self.autocommit, parameters=self.parameters)
        for output in self.hook.conn.notices:
            self.log.info(output)
        if self.delete is True:
            os.remove(sql_file)
