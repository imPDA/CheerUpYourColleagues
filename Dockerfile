FROM apache/airflow:2.8.1

COPY requirements.txt .

RUN pip install --upgrade pip &&\
    pip install apache-airflow[amazon,postgres]==${AIRFLOW_VERSION} &&\
    pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/opt"
