from airflow.decorators import dag, task
import pendulum

import requests
import xmltodict

from airflow.providers.sqlite.operators.sqlite import SqliteOperator

# Download podcast metadata


# all DAGs property
@dag(
    dag_id="podcast_summary",
    schedule_interval="@hourly",
    start_date=pendulum.datetime(2023, 4, 18),
    catchup=False,
)
# creating our first dataline
# contain all the logic of pipeline
# you should change airflow.cfg dags_folder
def podcast_summary():
    create_databases = SqliteOperator(
        task_id="create_table_sqlite",
        sql=r"""
        CREATE TABLE IF NOT EXISTS episodes(
            link TEXT PRIMARY KEY,
            title TEXT,
            filename TEXT,
            published TEXT,
            description TEXT
        )
        """,
    )

    @task()
    def get_episodes():
        data = requests.get("https://marketplace.org/feed/podcast/marketplace")
        feed = xmltodict.parse(data.text)
        episodes = feed["rss"]["channel"]["item"]
        print(f"Found {len(episodes)} episodes.")
        return episodes

    podcast_episodes = get_episodes()
    create_databases.set_downstream(podcast_episodes)


summary = podcast_summary()
