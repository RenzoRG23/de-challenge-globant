from .services import cs_csv_to_df, insert_into_bigquery, get_quarterly_hires, get_department_hires
from fastapi import APIRouter

router = APIRouter()

@router.get("/carga_historica")
async def carga_historica():
    bucket_name = "dev-globant-de"
    files_paths = [
    'departments/departments.csv',
    'employees/hired_employees.csv',
    'jobs/jobs.csv'
    ]

    for file_path in files_paths:
        df = cs_csv_to_df(bucket_name, file_path)

        # Construct the table_id based on the file_path
        if 'departments' in file_path:
            table_id = 'potent-result-414004.globant_de.raw_departments'
        elif 'employees' in file_path:
            table_id = 'potent-result-414004.globant_de.raw_hired_employees'
        elif 'jobs' in file_path:
            table_id = 'potent-result-414004.globant_de.raw_jobs'

        insert_into_bigquery(df, table_id)
    return "Carga historica realizada correctamente"

@router.post("/employees_hired_quarterly")
async def employees_hired_quarterly(request_data: dict):
    year = request_data.get("year")
    result = get_quarterly_hires(year)
    return result


@router.post("/departments_with_most_hires")
async def employees_hired_quarterly(request_data: dict):
    year = request_data.get("year")
    result = get_department_hires(year)
    return result