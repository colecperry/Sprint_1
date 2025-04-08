FROM python:3.11

# Create a new /app folder inside the container
WORKDIR /app

# Copy files from local src into app/src
COPY requirements.txt .
COPY src/requirements-dev.txt .
COPY src/ ./src/
COPY .env .

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Install deps
RUN pip install -r requirements.txt && pip install -r requirements-dev.txt

# Run the app (note the updated module path!)
CMD ["uvicorn", "src.CommonAssessmentTool.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

