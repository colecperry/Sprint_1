"""
Main application module for the Common Assessment Tool.
This module initializes the FastAPI application and includes all routers.
Handles database initialization and CORS middleware configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from CommonAssessmentTool.app import models
from CommonAssessmentTool.app.auth.router import router as auth_router
from CommonAssessmentTool.app.clients.router import router as clients_router
from CommonAssessmentTool.app.database import engine
from CommonAssessmentTool.app.ml.router import router as model_router


def setup_database():
    """Initializes database tables."""
    models.Base.metadata.create_all(bind=engine)


def create_app():
    """Creates and configures the FastAPI application."""
    app = FastAPI(
        title="Case Management API",
        description="API for managing client cases",
        version="1.0.0",
    )

    app.include_router(auth_router)
    app.include_router(clients_router)
    app.include_router(model_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    return app


# Initialize database and application
setup_database()
app = create_app()

