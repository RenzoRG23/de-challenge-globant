# Step 1: Use official lightweight Python image as base OS.
FROM tiangolo/uvicorn-gunicorn:python3.8-slim

# Step 2. Copy local code to the container image.
WORKDIR /app
COPY . .

# Step 3. Install production dependencies.
RUN pip install -r requirements.txt

# Step 4: Run the web service on container startup using gunicorn webserver.
EXPOSE 8000
ENV PORT=8000
ENV ENV_DEPLOY="prod"

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app
