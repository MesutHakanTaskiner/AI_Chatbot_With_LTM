import os
from database.init_db import init_db, LTMName, LTMDates, LTMProfession, LTMLocation, LTMPreferences, LTMPersonalDetails, LTMGoals, LTMSpecialDetails, LTMAdditionalDetails
from sqlalchemy.orm import sessionmaker
from operations.get_embedding import embedding_creator

# Initialize engine and sessionmaker using SQLAlchemy ORM
engine = init_db()
SessionLocal = sessionmaker(bind=engine)

db_file = "LTM.db"

def init_db_if_needed():
    # For SQLite, check if the database file exists (assumes DATABASE_URL of the form "sqlite:///LTM.db")
    if not os.path.exists(db_file):
        print("Database file not found. Initializing new database.")
        init_db()
    else:
        print("Database already exists.")

def check_ltm_data(ltm_info):
    """
    Processes ltm_info by joining list entries into strings.
    Returns a dictionary mapping field names to non-empty string values.
    """
    fields = ["name", "dates", "profession", "location", "preferences", "personal_details", "goals", "special_details", "additional_details"]
    data = {}
    for field in fields:
        value = " ".join(getattr(ltm_info, field, []))
        if value.strip():
            data[field] = value.strip()
    return data

def save_metadata(ltm_info):
    """
    Saves LTM information into corresponding tables.
    Only non-empty fields are saved.
    """
    processed_data = check_ltm_data(ltm_info)
    # Mapping of field names to corresponding ORM model
    field_model_map = {
        "name": LTMName,
        "dates": LTMDates,
        "profession": LTMProfession,
        "location": LTMLocation,
        "preferences": LTMPreferences,
        "personal_details": LTMPersonalDetails,
        "goals": LTMGoals,
        "special_details": LTMSpecialDetails,
        "additional_details": LTMAdditionalDetails
    }
    session = SessionLocal()
    for field, value in processed_data.items():
        model = field_model_map.get(field)
        if model:
            embedding = embedding_creator(value)
            record = model(value=value, embedding=embedding)
            session.add(record)
    session.commit()
    session.close()





