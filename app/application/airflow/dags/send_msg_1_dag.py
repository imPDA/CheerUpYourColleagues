from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from logic.send_random_message import send_random_image_and_text

with DAG(
    dag_id='send_quote_first_approach',
    schedule=None,
    tags=['cheer_up_your_colleagues'],
    description='lorem ipsum dolor sit amet, consectetur adipiscing',
    catchup=False,
) as first_approach:
    start = EmptyOperator(
        task_id='start',
    )

    execute_script = PythonOperator(
        task_id='send_message',
        python_callable=send_random_image_and_text,
    )

    end = EmptyOperator(
        task_id='end',
    )

    start >> execute_script >> end
