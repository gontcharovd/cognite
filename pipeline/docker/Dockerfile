FROM apache/airflow:2.0.0-python3.8
LABEL maintainer="Denis Gontcharov"

WORKDIR ${AIRFLOW_HOME}

# ENV VIRTUAL_ENV=/opt/airflow/env
# RUN python3 -m venv env
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# COPY requirements.txt .
COPY setup.sh .
# RUN pip install -r requirements.txt

USER airflow

VOLUME /tmp
