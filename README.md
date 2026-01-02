# Apache Airflow Educational Data Pipeline

## Project Overview

This project demonstrates an end-to-end **Big Data Pipeline** using Apache Airflow and Docker. It simulates a Data Lakehouse architecture where sales data moves through three distinct stages: **Raw**, **Processed** (Intermediate), and **Curated**.
The primary goal is to provide a hands-on example of orchestration, data validation, and transformation using a Local Executor setup.

## Architecture & Components

* 
**Orchestrator:** Apache Airflow (running in Docker).


* 
**Database:** PostgreSQL (handles Airflow metadata).


* 
**Execution Mode:** LocalExecutor.


* 
**Storage:** Local filesystem (mounted volumes) simulating the Data Lake layers.



## Repository Structure

The project file structure is organized as follows:

```plaintext
airflow-bigdata-pipeline/
├── docker-compose.yml        # Defines Airflow services (Webserver, Scheduler, DB)
├── dags/                     # Folder for DAG files
│   └── bigdata_pipeline.py   # Main pipeline definition
└── data/                     # Simulated Data Lake storage
    ├── raw/                  # Ingestion zone
    ├── processed/            # Cleaning zone
    └── curated/              # Final analytics zone

```

## Prerequisites

Before running the project, ensure you have the following installed:

* **Docker Engine**
* **Docker Compose**

## How to Run the Project

### 1. Start the Containers

Navigate to the project root directory and run the following command to download images and start the services (Postgres, Webserver, Scheduler, and Init):

```bash
docker-compose up -d

```

*Note: The `airflow-init` service defined in the docker-compose file will automatically initialize the database metadata.*

### 2. Create an Admin User

Since the default initialization only sets up the database, you must manually create an admin user to access the UI. Run this command once the containers are running:

```bash
docker-compose run --rm airflow-webserver airflow users create \
    --username airflow \
    --password airflow \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@airflow.local

```

### 3. Access the Airflow UI

Once the user is created, open your web browser and navigate to:

* 
**URL:** `http://localhost:8080` 


* **Username:** `airflow`
* **Password:** `airflow`

## Description of the DAG

The DAG is named **`daily_sales_lakehouse_pipeline`**. It orchestrates the flow of data across the simulated storage layers.

### Tasks Breakdown

1. **`extract_sales_task` (Ingest):**
* Simulates the extraction of data.
* Writes a CSV file (`sales.csv`) with sample data to the **Raw** layer (`data/raw/`).




2. **`validate_sales_task` (Validate):**
* Performs a data quality check.
* Verifies that `sales.csv` exists in the Raw layer before proceeding. Raises an error if data is missing.




3. **`transform_sales_task` (Transform):**
* Reads from Raw, cleans the data (simulated copy), and writes `sales_clean.csv` to the **Processed** layer (`data/processed/`).




4. **`load_curated_sales_task` (Load):**
* Moves the clean data to the **Curated** Data Lakehouse layer (`data/curated/`) as `sales_curated.csv`.




5. **`analytics_sales_task` (Analytics):**
* Simulates a BI/Machine Learning trigger by printing a success message indicating data is ready for consumption.





## Test Scenarios / How to Verify It Works

### 1. Manual Trigger

1. In the Airflow UI, locate the DAG `daily_sales_lakehouse_pipeline`.
2. Toggle the **Unpause** switch (to "On").


3. Click the **Trigger DAG** button (Play icon) in the Actions column.



### 2. Check Execution Status

Switch to the **Graph View**. You should see the tasks turn green (Success) sequentially:


`extract` -> `validate` -> `transform` -> `load` -> `analytics`.

### 3. Verify Output Files

Check your local project folder to verify the data flow. The following files should be generated:

* `./data/raw/sales.csv`
* `./data/processed/sales_clean.csv`
* `./data/curated/sales_curated.csv`

## Troubleshooting

* **Database not initialized:** If the webserver keeps restarting, ensure the `airflow-init` service completed successfully in the Docker logs.
* **Permission Errors:** If Python cannot write to the `data/` folder, ensure your local user has write permissions on the mounted `data` directory.
* **Port 8080 Conflict:** If you cannot access the UI, check if another service is using port 8080. You can map a different port in `docker-compose.yml` (e.g., `"8081:8080"`).
