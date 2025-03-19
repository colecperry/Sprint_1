import pandas as pd
import traceback
from sqlalchemy.orm import Session
from CommonAssessmentTool.app.database import SessionLocal
from CommonAssessmentTool.app.models import Client, User, ClientCase
from CommonAssessmentTool.app.enums import UserRole, GenderEnum
from CommonAssessmentTool.app.auth.router import get_password_hash
import os


def create_default_users(db: Session):
    """Creates default admin and case worker users if they do not exist."""
    users = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
            "role": UserRole.ADMIN,
        },
        {
            "username": "case_worker1",
            "email": "caseworker1@example.com",
            "password": "worker123",
            "role": UserRole.CASE_WORKER,
        },
    ]

    for user in users:
        print(f"Checking if {user['username']} exists in the database...")  # Debugging
        existing_user = db.query(User).filter(User.username == user["username"]).first()

        if not existing_user:
            print(f"Creating user: {user['username']}")  # Debugging
            new_user = User(
                username=user["username"],
                email=user["email"],
                hashed_password=get_password_hash(user["password"]),
                role=user["role"],
            )
            db.add(new_user)
            try:
                db.commit()
                print(f"✅ {user['username']} user created successfully")
            except Exception as commit_error:
                print(f"❌ Error committing {user['username']} to DB:", commit_error)
                db.rollback()
        else:
            print(f"✅ {user['username']} already exists in DB: {existing_user.email}")


def map_gender(value):
    """Maps integer gender values to GenderEnum values."""
    gender_mapping = {1: GenderEnum.MALE, 2: GenderEnum.FEMALE}
    return gender_mapping.get(value, None)  # Returns None if value is invalid


def load_client_data(db: Session):
    """Loads and processes client data from CSV into the database."""
    print("Loading CSV data...")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "app/clients/service/data_commontool.csv")

    df = pd.read_csv(csv_path)


    integer_columns = [
        "age",
        "gender",
        "work_experience",
        "canada_workex",
        "dep_num",
        "level_of_schooling",
        "reading_english_scale",
        "speaking_english_scale",
        "writing_english_scale",
        "numeracy_scale",
        "computer_scale",
        "housing",
        "income_source",
        "time_unemployed",
        "success_rate",
    ]
    df[integer_columns] = df[integer_columns].apply(pd.to_numeric, errors="raise")

    for _, row in df.iterrows():
        client = Client(
            age=int(row["age"]),
            gender=map_gender(int(row["gender"])),  # Convert integer to Enum
            work_experience=int(row["work_experience"]),
            canada_workex=int(row["canada_workex"]),
            dep_num=int(row["dep_num"]),
            canada_born=bool(row["canada_born"]),
            citizen_status=bool(row["citizen_status"]),
            level_of_schooling=int(row["level_of_schooling"]),
            fluent_english=bool(row["fluent_english"]),
            reading_english_scale=int(row["reading_english_scale"]),
            speaking_english_scale=int(row["speaking_english_scale"]),
            writing_english_scale=int(row["writing_english_scale"]),
            numeracy_scale=int(row["numeracy_scale"]),
            computer_scale=int(row["computer_scale"]),
            transportation_bool=bool(row["transportation_bool"]),
            caregiver_bool=bool(row["caregiver_bool"]),
            housing=int(row["housing"]),
            income_source=int(row["income_source"]),
            felony_bool=bool(row["felony_bool"]),
            attending_school=bool(row["attending_school"]),
            currently_employed=bool(row["currently_employed"]),
            substance_use=bool(row["substance_use"]),
            time_unemployed=int(row["time_unemployed"]),
            need_mental_health_support_bool=bool(
                row["need_mental_health_support_bool"]
            ),
        )
        db.add(client)
        db.commit()

        client_case = ClientCase(
            client_id=client.id,
            user_id=db.query(User)
            .filter(User.username == "admin")
            .first()
            .id,  # Assign to admin
            employment_assistance=bool(row["employment_assistance"]),
            life_stabilization=bool(row["life_stabilization"]),
            retention_services=bool(row["retention_services"]),
            specialized_services=bool(row["specialized_services"]),
            employment_related_financial_supports=bool(
                row["employment_related_financial_supports"]
            ),
            employer_financial_supports=bool(row["employer_financial_supports"]),
            enhanced_referrals=bool(row["enhanced_referrals"]),
            success_rate=int(row["success_rate"]),
        )
        db.add(client_case)
        db.commit()


def initialize_database():
    """Runs database initialization procedures."""
    print("Starting database initialization...")
    db = SessionLocal()
    try:
        create_default_users(db)
        load_client_data(db)
        print("✅ Database initialization completed successfully!")
    except Exception as e:
        print("❌ Error during initialization:")
        traceback.print_exc()  # This prints the full error message
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    initialize_database()
