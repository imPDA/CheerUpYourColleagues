import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from logic.image_processing import combine_and_save_to_s3
from logic.save_content import save_statistics
from logic.send_random_message import (
    get_random_image_url,
    get_random_quote,
    send_image_to_teams,
)
from logic.send_wednesday_meme import get_wednesday_meme_picture_url


def wednesday(date: pendulum.Date) -> bool:
    return date.day_of_week == 3


def get_image_url(ds) -> str:
    date = pendulum.from_format(ds, 'YYYY-MM-DD').date()
    return (
        get_wednesday_meme_picture_url() if wednesday(date) else get_random_image_url()
    )


def get_quote(ds) -> dict:
    date = pendulum.from_format(ds, 'YYYY-MM-DD').date()
    return (
        {'text': 'It`s Wednesday My Dudes!'} if wednesday(date) else get_random_quote()
    )


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

    combine_and_save_to_s3_task = PythonOperator(
        task_id='combine_and_save_to_s3',
        python_callable=combine_and_save_to_s3,
        op_kwargs={
            'picture_url': get_image_url_task.output,
            'quotation_dict': get_quote_task.output,
        },
    )

    send_message_task = PythonOperator(
        task_id='send_message',
        python_callable=send_image_to_teams,
        op_kwargs={
            'image_dict': combine_and_save_to_s3_task.output,
        },
    )

    save_quote_data_task = PythonOperator(
        task_id='save_quote_data',
        python_callable=save_statistics,
        op_kwargs={
            'quotation_dict': get_quote_task.output,
            'image_dict': combine_and_save_to_s3_task.output,
        },
    )

    end = EmptyOperator(task_id='end')

    (
        start
        >> [get_image_url_task, get_quote_task]
        >> send_message_task
        >> save_quote_data_task
        >> end
    )
