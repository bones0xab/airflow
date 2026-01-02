from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

RAW_DATA_DIR = "/opt/airflow/data/raw"
INTERMEDIATE_DATA_DIR = "/opt/airflow/data/processed"
CURATED_DATA_DIR = "/opt/airflow/data/curated"

def extract_sales_data():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    with open(f"{RAW_DATA_DIR}/sales.csv", "w") as sales_file:
        sales_file.write("client,amount\nA,100\nB,200\nA,150\nC,300")

def check_sales_data_presence():
    if not os.path.exists(f"{RAW_DATA_DIR}/sales.csv"):
        raise ValueError("Données manquantes")

def cleanse_sales_data():
    os.makedirs(INTERMEDIATE_DATA_DIR, exist_ok=True)
    with open(f"{RAW_DATA_DIR}/sales.csv") as raw_sales_file, \
        open(f"{INTERMEDIATE_DATA_DIR}/sales_clean.csv", "w") as cleaned_sales_file:
        cleaned_sales_file.write(raw_sales_file.read())

def publish_to_curated_layer():
    os.makedirs(CURATED_DATA_DIR, exist_ok=True)
    with open(f"{INTERMEDIATE_DATA_DIR}/sales_clean.csv") as cleaned_sales_file, \
        open(f"{CURATED_DATA_DIR}/sales_curated.csv", "w") as curated_sales_file:
        curated_sales_file.write(cleaned_sales_file.read())

def run_analytics_stage():
    print("Données prêtes pour BI / Machine Learning")

with DAG(
    dag_id="daily_sales_lakehouse_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    description="End-to-end sales data pipeline orchestrated with Airflow"
) as sales_data_pipeline_dag:
    ingest_sales_task = PythonOperator(
        task_id="extract_sales_task",
        python_callable=extract_sales_data
    )
    validate_sales_task = PythonOperator(
        task_id="validate_sales_task",
        python_callable=check_sales_data_presence
    )
    transform_sales_task = PythonOperator(
        task_id="transform_sales_task",
        python_callable=cleanse_sales_data
    )
    load_curated_sales_task = PythonOperator(
        task_id="load_curated_sales_task",
        python_callable=publish_to_curated_layer
    )
    analytics_sales_task = PythonOperator(
        task_id="analytics_sales_task",
        python_callable=run_analytics_stage
    )

    ingest_sales_task >> validate_sales_task >> transform_sales_task >> load_curated_sales_task >> analytics_sales_task
