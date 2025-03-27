from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///LTM.db"

Base = declarative_base()

class LTMName(Base):
    __tablename__ = "ltm_names"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    embedding = Column(String)

class LTMDates(Base):
    __tablename__ = "ltm_dates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    embedding = Column(String)

class LTMProfession(Base):
    __tablename__ = "ltm_professions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    embedding = Column(String)

class LTMLocation(Base):
    __tablename__ = "ltm_locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    embedding = Column(String)

class LTMPersonalDetails(Base):
    __tablename__ = "ltm_personal_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    embedding = Column(String)

class LTMGoals(Base):
    __tablename__ = "ltm_goals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    embedding = Column(String)

class LTMSpecialDetails(Base):
    __tablename__ = "ltm_special_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    embedding = Column(String)

class LTMAdditionalDetails(Base):
    __tablename__ = "ltm_additional_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    embedding = Column(String)

def init_db():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    engine = init_db()
    print("Database initialized using SQLAlchemy ORM.")
