from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from logic.send_random_message import (
    get_random_image_url,
    get_random_quote,
    send_image_and_quote_to_teams,
)


@dag(
    dag_id='send_quote_second_approach_taskflow',
    schedule=None,
    tags=['cheer_up_your_colleagues'],
    description='lorem ipsum dolor sit amet, consectetur adipiscing',
    catchup=False,
)
def send_quote_second_approach_taskflow():
    get_image_url = task()(get_random_image_url)
    get_quote = task()(get_random_quote)
    send_message = task()(send_image_and_quote_to_teams)

    end = EmptyOperator(
        task_id='end',
    )

    send_message(get_quote(), get_image_url()) >> end


send_quote_second_approach_taskflow()
