# Airflow_podcast

Overview 
This program helps you download 'Podcast' files regularly using 'Airflow'


Steps

1. You have to install Apache-airflow version 2.3.1, python version 3.9 ,and 'apache-airflow[pandas]'
2. run airflow server / airflow standalone
3. trigger task / airflow dags trigger podcast_summary
4. mkdir episodes where mp3 files will be stored
5. type code
6. connect db
  1) sqlite3 episodes.db
  2) .databases / to make db
  3) type this in terminal to connect airflow and db / airflow connections add 'podcasts' --conn-type 'sqlite' --conn-host 'episodes.db'
  4) check connection / airflow connections get podcasts
