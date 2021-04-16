airflow-init: 
				mkdir -p pipeline/airflow/logs/
				mkdir -p pipeline/airflow/plugins/
				mkdir -p pipeline/airflow/tmp/
				sudo chmod -R 777 pipeline/airflow/logs/
				sudo chmod -R 777 pipeline/airflow/plugins/
				sudo chmod -R 777 pipeline/airflow/tmp/
				docker-compose up airflow-init
				sudo chmod -R 777 pipeline/postgresql/
