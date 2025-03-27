import os
import sqlite3
from database.init_db import init_db
from datetime import datetime
import json

db_path = "ltm.db"

def init_db_if_needed(db_path=db_path):
    if not os.path.exists(db_path):
        print("Database file not found. Initializing new database.")
        init_db(db_path)
    else:
        print("Database already exists.")

# Placeholder for saving data into the database
def save_metadata(ltm_info):

    ltm_name = (" ").join(ltm_info.name)
    ltm_dates = (" ").join(ltm_info.dates)
    ltm_profession = (" ").join(ltm_info.profession)
    ltm_location = (" ").join(ltm_info.location)
    ltm_preferences = (" ").join(ltm_info.preferences)
    ltm_personal_details = (" ").join(ltm_info.personal_details)
    ltm_goals = (" ").join(ltm_info.goals)
    ltm_special_details = (" ").join(ltm_info.special_details)


    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_details (name, dates, profession, location, preferences, personal_details, goals, special_details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ltm_name, ltm_dates, ltm_profession, ltm_location, ltm_preferences, ltm_personal_details, ltm_goals, ltm_special_details))


    conn.commit()
    conn.close()

# Placeholder for updating data in the database
def update_data(data):
    # Implement update functionality here
    pass
