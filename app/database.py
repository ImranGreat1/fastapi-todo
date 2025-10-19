from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://user@localhost:5432/fastapi_todo"

engine = create_engine(DATABASE_URL, echo=True)

# create connection to the database
Session = sessionmaker(autoflush=False, bind=engine)

# base class for models 
Base = declarative_base()


def get_db():
    # create a new session
    db = Session()

    try:
        # yeild = return db for use inside request
        yield db
    finally:
        # Close session after request finishes
        db.close()