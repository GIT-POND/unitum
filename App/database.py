from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# working with environment variables
from .config import settings as set

# SAMPLE_URL = 'postgresql://User_name:Password@DB_ipAddress:Port_num/DB_name'
DATABASE_URL = f'postgresql://{set.database_username}:{set.database_password}@{set.database_host}:{set.database_port}/{set.database_name}'

engine = create_engine(DATABASE_URL)  # establish connection to db
localSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# * Dependency
def get_db():
    ''' NOTE: Function creates a db session when a http request is revieved'''
    db = localSession()

    try:
        yield db
    finally:
        db.close()