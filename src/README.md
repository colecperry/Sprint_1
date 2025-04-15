# 📌 CommonAssessmentTool

A Python-based backend for case management with FastAPI, PostgreSQL, and SQLAlchemy.

---

## 🛠️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
$ git clone <repository_url>
$ cd CommonAssessmentTool

2️⃣ Create & Activate a Virtual Environment
$ python3 -m venv .venv # Create a virtual environment (only do this once per project)
$ source .venv/bin/activate  # macOS/Linux
$ .venv\Scripts\activate # Windows

3️⃣ Install Dependencies
$ pip install -r requirements.txt # Only install dependencies once per project
$ pip install -e . # Installs requirements-dev.txt file

📦 Building the Project
$ pip install build
$ python -m build

🚀 Starting the Backend
1️⃣ Set PYTHONPATH
$ export PYTHONPATH=$PWD/src
$ uvicorn CommonAssessmentTool.app.main:app --reload
# server will be avaiable at : http://127.0.0.1:8000
# Avaiable endpoints: 
    # GET -> /models/available -> list available model names
    # GET -> /models/current -> Get the current active model names
    # POST -> /models/select -> Switch the active model
    # POST -> /models/predict -> Make a prediction with input features

3️⃣ Open API Docs -> For local testing
http://127.0.0.1:8000/docs # provides an interactice API documentation with all available endpoints

🧪 Running Tests
1️⃣ Ensure PYTHONPATH is Set
$ export PYTHONPATH=$PWD/src

2️⃣ Run Unit Tests
$ pytest tests/ # Run it from inside src/CommonAssessmentTool
OR
$ python -m pytest tests/

3️⃣ Run Test Coverage Report
$ pytest --cov=src/CommonAssessmentTool tests/

🔍 Linting & Code Quality Checks
1️⃣ Run black for Formatting
$ black --check src/ # Check
$ black src/ # Fix

2️⃣ Run flake8 for Style Issues
$ flake8 src/

3️⃣ Run pylint for Code Smells
$ pylint src/

4️⃣ Run mypy for Type Checking
$ mypy src/

💾 Database Setup & Initialization
1️⃣ Run the Database Initialization Script
$ export PYTHONPATH=$PWD/src
$ python -m CommonAssessmentTool.initialize_data

## 🚀 Running the Backend with Docker
### 🐳 Docker (no Compose)

$ docker build -t coles_image -f src/Dockerfile .
$ docker run -d -p 8000:8000 coles_image

# Docker Compose (Local Only)
$ docker-compose up --build # App will be available at http://localhost:8000

# TO STOP
CRTL + C
$ docker-compose down

🌍 Public Deployment (AWS EC2)
To deploy to a public endpoint
1. Launch an EC2 instance (Ubuntu 22.04, t2.micro)
2. SSH into it: 
    $ ssh -i ~/.ssh/my-ec2-key.pem ubuntu@<your-ec2-ip>
3. Install Docker: 
    $ sudo apt update
    $ sudo apt install -y docker.io
    $ sudo usermod -aG docker ubuntu
4. Copy project to server and run:
    $ docker build -t coles_image -f src/Dockerfile .
    $ docker run -d -p 8000:8000 coles_image
5. Swagger docs will be available at: http://<your-ec2-ip>:8000/docs


🔄 Committing Changes to Git
1️⃣ Bypass Pre-Commit Hooks (if needed)
$ git commit -m "Your commit message" --no-verify
$ git push origin main
$ deactivate # Deactivate virtual environment before exiting

