import os
from database.init_db import init_db, LTMName, LTMDates, LTMProfession, LTMLocation, LTMPreferences, LTMPersonalDetails, LTMGoals, LTMSpecialDetails, LTMAdditionalDetails
from sqlalchemy.orm import sessionmaker
from operations.embedding import get_embedding

# Initialize engine and sessionmaker using SQLAlchemy ORM
engine = init_db()
SessionLocal = sessionmaker(bind=engine)

db_file = "LTM.db"

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
    
    session = SessionLocal()
    for field, value in processed_data.items():
        model = field_model_map.get(field)
        if model:
            embedding = get_embedding(value)
            record = model(value=value, embedding=embedding)
            session.add(record)
    session.commit()
    session.close()

def get_ltm_data_from_db():
    """
    Retrieves all LTM data from the database. if not empty
    Returns a dictionary mapping field names to lists of values.
    """
    session = SessionLocal()
    ltm_data = {
        "name": [name.value for name in session.query(LTMName).all()],
        "dates": [dates.value for dates in session.query(LTMDates).all()],
        "profession": [profession.value for profession in session.query(LTMProfession).all()],
        "location": [location.value for location in session.query(LTMLocation).all()],
        "preferences": [preferences.value for preferences in session.query(LTMPreferences).all()],
        "personal_details": [personal_details.value for personal_details in session.query(LTMPersonalDetails).all()],
        "goals": [goals.value for goals in session.query(LTMGoals).all()],
        "special_details": [special_details.value for special_details in session.query(LTMSpecialDetails).all()],
        "additional_details": [additional_details.value for additional_details in session.query(LTMAdditionalDetails).all()]
    }

    # Remove empty lists
    ltm_data = {field: values for field, values in ltm_data.items() if values}

    session.close()
    return ltm_data

def delete_ltm_data(data):
    # delete ltm data according to key
    session = SessionLocal()
    
    model = field_model_map.get(data["key"])
    if model:
        session.query(model).filter(model.value == data["value"]).delete()

    session.commit()
    session.close()

    return "Data deleted successfully"



