from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from logic.send_random_message import (
    get_random_image_url,
    get_random_quote,
    send_image_and_quote_to_teams,
)

with DAG(
    dag_id='msi_project_dag',
    schedule=None,
    tags=['cheer_up_your_colleagues', 'MSI'],
    description='Main DAG of Mental State Improvement project',
    catchup=False,
) as msi_project_dag:
    start = EmptyOperator(task_id='start')

    get_image_url = PythonOperator(
        task_id='get_random_image_url',
        python_callable=get_random_image_url,
    )

    get_quote = PythonOperator(
        task_id='get_random_quote',
        python_callable=get_random_quote,
    )

    send_message = PythonOperator(
        task_id='send_message',
        python_callable=send_image_and_quote_to_teams,
        op_args=[get_quote.output, get_image_url.output],
    )

    end = EmptyOperator(task_id='end')

    start >> [get_image_url, get_quote] >> send_message >> end
