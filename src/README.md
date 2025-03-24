# 📌 CommonAssessmentTool

A Python-based backend for case management with FastAPI, PostgreSQL, and SQLAlchemy.

---

## 🛠️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
$ git clone <repository_url>
$ cd CommonAssessmentTool

2️⃣ Create & Activate a Virtual Environment
$ python3 -m venv .venv
$ source .venv/bin/activate  # macOS/Linux
$ .venv\Scripts\activate # Windows

3️⃣ Install Dependencies
$ pip install -r requirements.txt
$ pip install -e . # Installs requirements-dev.txt file

📦 Building the Project
$ pip install build
$ python -m build

🚀 Starting the Backend
1️⃣ Set PYTHONPATH
$ export PYTHONPATH=$PWD/src
$ uvicorn CommonAssessmentTool.app.main:app --reload
# server will be avaiable at : http://127.0.0.1:8000

3️⃣ Open API Docs
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

🔄 Committing Changes to Git
1️⃣ Bypass Pre-Commit Hooks (if needed)
$ git commit -m "Your commit message" --no-verify
$ git push origin main
$ deactivate # Deactivate virtual environment before exiting