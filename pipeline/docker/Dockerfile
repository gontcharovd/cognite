FROM python:3.8
LABEL maintainer="Denis"

ARG AIRFLOW_USER_HOME=/home/pipeline
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

RUN apt update
RUN apt install -y python3-pip python3-venv supervisor

WORKDIR ${AIRFLOW_HOME}
ENV VIRTUAL_ENV=/home/pipeline/env
RUN python3 -m venv env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir tmp
ENV TMP_PATH=tmp

COPY dag/pressure_dag.py ${AIRFLOW_HOME}/dags/pressure_dag.py
COPY dag/custom_airflow/ ${AIRFLOW_HOME}/dags/custom_airflow/
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

RUN airflow initdb

COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"] 
