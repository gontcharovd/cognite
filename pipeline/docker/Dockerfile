FROM apache/airflow:2.0.0-python3.8
LABEL maintainer="Denis Gontcharov"

RUN pip3 install --upgrade pip \
  && pip3 install 'apache-airflow-providers-postgres' cognite-sdk

WORKDIR ${AIRFLOW_HOME}

USER airflow

VOLUME /tmp

COPY setup.sh ./setup.sh
