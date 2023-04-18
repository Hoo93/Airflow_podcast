from airflow.decorators import dag, task
import pendulum


# Download podcast metadata


@dag(
    dag_id="podcast_summary",
    schedule_interval="@daily",
    start_date=pendulum.datetime(2023, 4, 18),
    catchup=False,
)
def podcast_summary2():
    pass
