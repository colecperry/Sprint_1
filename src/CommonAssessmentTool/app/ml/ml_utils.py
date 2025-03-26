# app/ml/ml_utils.py

import pandas as pd
from sqlalchemy.orm import Session
from CommonAssessmentTool.app.models import Client, ClientCase

def extract_features_and_labels(db: Session):
    joined = db.query(Client, ClientCase).join(ClientCase, Client.id == ClientCase.client_id).all()

    features, labels = [], []

    for client, case in joined:
        features.append([
            client.age,
            client.work_experience,
            client.canada_workex,
            client.dep_num,
            int(client.canada_born),
            int(client.citizen_status),
            client.level_of_schooling,
            int(client.fluent_english),
            client.reading_english_scale,
            client.speaking_english_scale,
            client.writing_english_scale,
            client.numeracy_scale,
            client.computer_scale,
            int(client.transportation_bool),
            int(client.caregiver_bool),
            client.housing,
            client.income_source,
            int(client.felony_bool),
            int(client.attending_school),
            int(client.currently_employed),
            int(client.substance_use),
            client.time_unemployed,
            int(client.need_mental_health_support_bool),
        ])
        labels.append(1 if case.success_rate >= 70 else 0) # Client will be successful if success rate > 70%

    return pd.DataFrame(features), pd.Series(labels)
