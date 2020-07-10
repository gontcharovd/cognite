import airflow
from urllib import request
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator

dag = DAG(
    'stocksense',
    start_date=airflow.utils.dates.days_ago(10),
    schedule_interval='@daily',
    template_searchpath='/tmp'
)


def _get_data(year, month, day, hour, output_path, **context):
    url = (
        'https://dumps.wikimedia.org/other/pageviews/'
        f'{year}/{year}-{month:0>2}/pageviews'
        f'-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz'
    )
    request.urlretrieve(url, output_path)


get_data = PythonOperator(
    task_id='get_data',
    python_callable=_get_data,
    provide_context=True,
    op_kwargs={
        'year': '{{ execution_date.year }}',
        'month': '{{ execution_date.month }}',
        'day': '{{ execution_date.day }}',
        'hour': '{{ execution_date.hour }}',
        'output_path': '/tmp/wikipageviews.gz',
    },
    dag=dag,
)

extract_gz = BashOperator(
    task_id='extract_gz',
    bash_command='gunzip --force /tmp/wikipageviews.gz',
    dag=dag
)


def _fetch_pageviews(pagenames, execution_date, **_):
    result = dict.fromkeys(pagenames, 0)
    with open('/tmp/wikipageviews', 'r') as f:
        for line in f:
            domain_code, page_title, view_counts, _ = line.split(' ')
            if domain_code == 'en' and page_title in pagenames:
                result[page_title] = view_counts
    with open('/tmp/postgres_query.sql', 'w') as f:
        for pagename, pageviewcount in result.items():
            f.write(
                'INSERT INTO pageview_counts VALUES ('
                f"'{pagename}', {pageviewcount}, '{execution_date}'"
                ');\n'
            )


fetch_pageviews = PythonOperator(
    task_id='fetch_pageviews',
    python_callable=_fetch_pageviews,
    op_kwargs={
        'pagenames': {
            'Google',
            'Amazon',
            'Apple',
            'Microsoft',
            'Facebook'
        },
        'execution_date': '{{ds}}'
    },
    provide_context=True,
    dag=dag
)

write_to_postgres = PostgresOperator(
   task_id='write_to_postgres',
   postgres_conn_id='stocksense',
   sql='postgres_query.sql',
   dag=dag
)

get_data >> extract_gz >> fetch_pageviews >> write_to_postgres

