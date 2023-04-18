from airflow.decorators import dag, task
import pendulum

import requests
import xmltodict

# Download podcast metadata


@dag(
    dag_id="podcast_summary",
    schedule_interval="@hourly",
    start_date=pendulum.datetime(2023, 4, 18),
    catchup=False,
)
# creating our first dataline
# comtain all the logic of pipline
def podcast_summary():
    # create operator s s
    @task()
    def get_episodes():
        data = requests.get("https://marketplace.org/feed/podcast/marketplace")
        feed = xmltodict.parse(data.text)
        episodes = feed["rss"]["channel"]["item"]
        print(f"Found {len(episodes)} episodes.")
        return episodes

    podcast_episodes = get_episodes()


summary = podcast_summary()
