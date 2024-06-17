from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, ShortCircuitOperator
from airflow.utils.trigger_rule import TriggerRule

from logic.send_random_message import (
    get_random_image_url,
    get_random_quote,
    send_image_and_quote_to_teams,
)


def do_run_today(ds: str) -> bool:
    mm_dd = ds.split('-', 1)[1]
    return mm_dd not in {'11-06', '13-06', '15-06', '25-06'}


with DAG(
    dag_id='msi_project_dag',
    schedule=None,
    tags=['cheer_up_your_colleagues', 'MSI'],
    description='Main DAG of Mental State Improvement project',
    catchup=False,
) as msi_project_dag:
    start = EmptyOperator(task_id='start')

    skip_on_holidays = ShortCircuitOperator(
        task_id='skip_on_holidays',
        python_callable=do_run_today,
        ignore_downstream_trigger_rules=False,
    )

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

    end = EmptyOperator(task_id='end', trigger_rule=TriggerRule.NONE_FAILED)

    start >> skip_on_holidays >> [get_image_url, get_quote] >> send_message >> end
