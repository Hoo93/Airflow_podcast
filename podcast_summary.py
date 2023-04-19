from airflow.decorators import dag, task
import pendulum

import requests
import xmltodict

from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.sqlite.hooks.sqlite import SqliteHook

# Download podcast metadata


PODCAST_URL = "https://marketplace.org/feed/podcast/marketplace"


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
    create_database = SqliteOperator(
        task_id="create_table_sqlite",
        sql=r"""
        CREATE TABLE IF NOT EXISTS episodes (
            link TEXT PRIMARY KEY,
            title TEXT,
            filename TEXT,
            published TEXT,
            description TEXT
        );
        """,
        sqlite_conn_id="podcasts",
    )

    # Decoration turns function into Airflow Task
    @task()
    def get_episodes():
        data = requests.get(PODCAST_URL)
        feed = xmltodict.parse(data.text)
        episodes = feed["rss"]["channel"]["item"]
        print(f"Found {len(episodes)} episodes.")
        return episodes

    podcast_episodes = get_episodes()
    create_database.set_downstream(podcast_episodes)


summary = podcast_summary()
# @task()
# def load_episodes(episodes):
#     hook = SqliteHook(sqlite_conn_id="podcasts")
#     stored = hook.get_pandas_df("SELECT * from episodes;")
#     new_episodes = []
#     for episode in episodes:
#         if episode["link"] not in stored["link"].values:
#             filename = f"{episode['link'].split('/')[-1]}.smp3"
#             new_episodes.append(
#                 [
#                     episode["link"],
#                     episode["titlde"],
#                     episode["pubDate"],
#                     episode["description"],
#                     filename,
#                 ]
#             )

#     hook.insert_rows(
#         table="episodes",
#         rows=new_episodes,
#         target_fields=[
#             "link",
#             "title",
#             "published",
#             "description",
#             "filename",
# ],
#     )

# load_episodes(podcast_episodes)
