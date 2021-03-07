import os

from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.utils.decorators import apply_defaults


class PostgresFileOperator(PostgresOperator):
    """Extends the PostgresOperator to read sql from a templated file path.

    The file is deletd if the upload succeeds and `delete` is True.

    Args:
        sql_file: (templated) path to a file containing SQL-statements
        delete: delete the `sql_file` after successful upload or not
    """
    template_fields = ('sql_file', )

    @apply_defaults
    def __init__(self, sql_file: str, delete: bool, **kwargs) -> None:
        super().__init__(sql=None, **kwargs)
        self.sql_file = sql_file
        self.delete = delete

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        self.hook = PostgresHook(
            postgres_conn_id=self.postgres_conn_id, schema=self.database)
        with open(self.sql_file, 'r') as f:
            sql = f.read(f)
        self.hook.run(sql, self.autocommit, parameters=self.parameters)
        for output in self.hook.conn.notices:
            self.log.info(output)
        if self.delete is True:
            os.remove(self.sql_file)
