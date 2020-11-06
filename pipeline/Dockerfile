FROM python:3.8

RUN apt update
RUN apt install -y python3-pip python3-venv supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /home/pipeline

ENV VIRTUAL_ENV=/home/pipeline/env
RUN python3 -m venv env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir tmp
ENV TMP_PATH=/home/pipeline/tmp

ENV AIRFLOW_HOME=/home/pipeline/airflow
RUN airflow initdb
COPY dag/pressure_dag.py airflow/dags/pressure_dag.py

CMD ["/usr/bin/supervisord"] 
