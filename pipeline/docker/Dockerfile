FROM apache/airflow:2.0.0-python3.8
LABEL maintainer="Denis Gontcharov"

RUN pip3 install --upgrade pip \
  && pip3 install 'apache-airflow-providers-postgres'

WORKDIR ${AIRFLOW_HOME}

USER airflow

VOLUME /tmp
# ENV VIRTUAL_ENV=/opt/airflow/env
# RUN python3 -m venv env
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# COPY requirements.txt .
# RUN pip install -r requirements.txt
COPY setup.sh .
