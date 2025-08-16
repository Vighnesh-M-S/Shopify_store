from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from app.db import DATABASE_URL, Base, engine
import app.models_db  # make sure models are imported

def init_db():
    # ✅ Create DB if it does not exist
    if not database_exists(engine.url):
        create_database(engine.url)
        print("Database created!")

    # ✅ Create all tables
    Base.metadata.create_all(bind=engine)
    print("Tables created!")

if __name__ == "__main__":
    init_db()
