echo "checking if Airflow metastore and Webserver user exist"
(airflow users list &&
  echo "Airflow metastore and Webserver user found. Skipping initialization") || (
echo "Initializing Airflow metastore and creating Airflow Webserver user"
airflow db init &&
  airflow users create \
    --role Admin \
    --username "${_AIRFLOW_WWW_USER_USERNAME}" \
    --password "${_AIRFLOW_WWW_USER_PASSWORD}" \
    --email "${_AIRFLOW_WWW_USER_EMAIL}" \
    --firstname "${_AIRFLOW_WWW_USER_FIRSTNAME}" \
    --lastname "${_AIRFLOW_WWW_USER_LASTNAME}"
)
