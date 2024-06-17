import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from logic.send_random_message import (
    get_random_image_url,
    get_random_quote,
    send_image_and_quote_to_teams,
)
from logic.send_wednesday_meme import get_wednesday_meme_picture_url


def wednesday(date: pendulum.Date) -> bool:
    return date.day_of_week == 2


def get_image_url(ds):
    date = pendulum.from_format(ds, 'YYYY-MM-DD').date()
    return (
        get_wednesday_meme_picture_url() if wednesday(date) else get_random_image_url()
    )


def get_quote(ds):
    date = pendulum.from_format(ds, 'YYYY-MM-DD').date()
    return 'It`s Wednesday My Dudes!' if wednesday(date) else get_random_quote()


with DAG(
    dag_id='msi_project_dag',
    schedule=None,
    tags=['cheer_up_your_colleagues', 'MSI'],
    description='Main DAG of Mental State Improvement project',
    catchup=False,
) as msi_project_dag:
    start = EmptyOperator(task_id='start')

    get_image_url_task = PythonOperator(
        task_id='get_image_url',
        python_callable=get_image_url,
    )

    get_quote_task = PythonOperator(
        task_id='get_quote',
        python_callable=get_quote,
    )

    send_message_task = PythonOperator(
        task_id='send_message',
        python_callable=send_image_and_quote_to_teams,
        op_kwargs={
            'quote': get_quote_task.output,
            'image_url': get_image_url_task.output,
        },
    )

    end = EmptyOperator(task_id='end')

    start >> [get_image_url_task, get_quote_task] >> send_message_task >> end
