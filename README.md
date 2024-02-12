# Globant Data Engineering Coding Challenge Solution

This repository hosts the solution to the Globant Data Engineering Coding Challenge. It features a FastAPI application designed for database migration tasks and analytical querying, fully deployed on Google Cloud Platform (GCP).

## Features

- **Database Migration API**: Receives CSV data, uploads to Google Cloud Storage, and inserts into BigQuery.
- **Analytical Endpoints**: Provides insights into employee hiring trends and departmental performance.
- **Cloud-Native Deployment**: Utilizes Docker for containerization and Google Cloud Run for scalable hosting.

## Workflow

![Challenge 1 Flow](.\images\DE_Challenge_1.drawio.png)

## Project Structure

- `main.py`: Entry point for the FastAPI application.
- `app/routes.py`: Defines API endpoints.
- `app/services.py`: Contains logic for CSV processing and BigQuery interaction.
- `Dockerfile`: Specifications for Docker containerization.
- `deploy.sh`: Shell script for simplified GCP deployment.

## Setup & Deployment

### Prerequisites

- Google Cloud SDK
- Docker
- Python environment

### Local Development

1. Clone the repo:

git clone <repository-url>

2. Install dependencies:

pip install -r requirements.txt

3. Run the application:

uvicorn main:app --reload

### Service Account

The service account must have the necessary access to the bucket on cloud storage and also for querying the tables on bigquery. In my case I have used the following ones: Bigquery Editor, Bigquery Job User, Cloud Storage Object Admin 

### Cloud Deployment

Execute `deploy.sh` to deploy to Google Cloud Run, ensuring GCP permissions are set correctly.

## API Endpoints

- `/carga_historica`: Initiates historical data loading.
- `/employees_hired_quarterly`: Fetches quarterly hiring statistics.
- `/departments_with_most_hires`: Identifies top hiring departments.

## Notes

Configure GCP credentials, project ID, and region in `deploy.sh`. Update the service account as needed.

## Author

- **Renzo Richle**
  - LinkedIn: [Renzo Richle](<https://www.linkedin.com/in/renzorichle23/>)
  - GitHub: [RenzoRG23](<https://github.com/RenzoRG23>)
  - Email: [renzorichleg23@gmail.com](mailto:renzorichleg23@gmail.com)

⭐️ From [RenzoRG23](<https://github.com/RenzoRG23>)
