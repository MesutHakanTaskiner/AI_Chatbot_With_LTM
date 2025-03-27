import os
from database.init_db import init_db, LTMName, LTMDates, LTMProfession, LTMLocation, LTMEducation, LTMPersonalDetails, LTMGoals, LTMSpecialDetails, LTMSocialInfo, LTMAdditionalDetails
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
        "education": LTMEducation,
        "personal_details": LTMPersonalDetails,
        "goals": LTMGoals,
        "special_details": LTMSpecialDetails,
        "social_info": LTMSocialInfo,
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
    fields = ["name", "dates", "profession", "location", "personal_details", "goals", "special_details", "additional_details"]
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
            # if value exists in the database then update the value and embedding
            if session.query(model).filter(model.value == value).first():
                pass

            # if value does not exist in the database then add the value and embedding
            else:
                
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
        "name": [record.value for record in session.query(LTMName).all()],
        "dates": [record.value for record in session.query(LTMDates).all()],
        "profession": [record.value for record in session.query(LTMProfession).all()],
        "location": [record.value for record in session.query(LTMLocation).all()],
        "education": [record.value for record in session.query(LTMEducation).all()],
        "personal_details": [record.value for record in session.query(LTMPersonalDetails).all()],
        "goals": [record.value for record in session.query(LTMGoals).all()],
        "special_details": [record.value for record in session.query(LTMSpecialDetails).all()],
        "social_info": [record.value for record in session.query(LTMSocialInfo).all()],
        "additional_details": [record.value for record in session.query(LTMAdditionalDetails).all()]
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

def update_ltm_data(data):
    # update ltm data according to key
    session = SessionLocal()

    print("update data", data)
    
    model = field_model_map.get(data["key"])
    if model:
        session.query(model).filter(model.value == data["old_value"]).update({"value": data["new_value"]})
        embed = get_embedding(data["new_value"])
        session.query(model).filter(model.value == data["old_value"]).update({"embedding": embed})

    session.commit()
    session.close()

    return "Data updated successfully"



