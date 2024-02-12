import io
import pandas as pd
from google.cloud import storage, bigquery

def cs_csv_to_df(bucket_name, source_blob_name):
    storage_client = storage.Client()
    # Define column names based on the expected CSV schema
    column_names = {
        'departments/departments.csv': ['id', 'department'],
        'employees/hired_employees.csv': ['id', 'name', 'datetime', 'department_id', 'job_id'],
        'jobs/jobs.csv': ['id', 'job']
    }

    # Get the appropriate column names for the current CSV file
    columns = column_names[source_blob_name]

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    data = blob.download_as_bytes()
    df = pd.read_csv(io.BytesIO(data), names=columns, header=None)
    return df

def insert_into_bigquery(df,table_id):
    # Initialize a BigQuery client
    client = bigquery.Client()

    # Define the job configuration
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True  # Automatically detect schema from DataFrame
    )

    # Insert data into the BigQuery table
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete

    print(f"Inserted {len(df)} rows into {table_id}")


def get_quarterly_hires(year):
    # Initialize a BigQuery client
    client = bigquery.Client()

    query = f"""
    SELECT 
        d.department,
        j.job,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM TIMESTAMP(e.datetime)) = 1 THEN e.id END) AS Q1,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM TIMESTAMP(e.datetime)) = 2 THEN e.id END) AS Q2,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM TIMESTAMP(e.datetime)) = 3 THEN e.id END) AS Q3,
        COUNT(CASE WHEN EXTRACT(QUARTER FROM TIMESTAMP(e.datetime)) = 4 THEN e.id END) AS Q4
    FROM `potent-result-414004.globant_de.raw_hired_employees` e

    INNER JOIN `potent-result-414004.globant_de.raw_departments` d 
    ON e.department_id = d.id

    INNER JOIN `potent-result-414004.globant_de.raw_jobs` j 
    ON e.job_id = j.id

    WHERE EXTRACT(YEAR FROM TIMESTAMP(e.datetime)) = {year} 
    GROUP BY 1, 2
    ORDER BY 1, 2
    """

    query_job = client.query(query)  # Make an API request.
    results = query_job.result()  # Wait for the job to complete.

    # Convert the results to a list of dicts to return as JSON
    data = [dict(row) for row in results]

    return data

def get_department_hires(year):
    # Initialize a BigQuery client
    client = bigquery.Client()

    query = f"""
    WITH DepartmentHires AS (
    SELECT 
        d.id AS department_id,
        d.department,
        COUNT(e.id) AS hires
    FROM `potent-result-414004.globant_de.raw_departments` d
    INNER JOIN `potent-result-414004.globant_de.raw_hired_employees` e 
        ON d.id = e.department_id
    WHERE EXTRACT(YEAR FROM TIMESTAMP(e.datetime)) = {year}
    GROUP BY 1, 2
    ),
    AverageHires AS (
    SELECT 
        AVG(hires) AS avg_hires
    FROM 
        DepartmentHires
    )
    SELECT 
    dh.department_id,
    dh.department,
    dh.hires
    FROM DepartmentHires dh, AverageHires ah
    WHERE dh.hires > ah.avg_hires
    ORDER BY 3 DESC
    """

    query_job = client.query(query)  # Make an API request.
    results = query_job.result()  # Wait for the job to complete.

    # Convert the results to a list of dicts to return as JSON
    data = [dict(row) for row in results]

    return data