from sqlmodel import create_engine

from src.core.env_vars import db_user,db_password, db_host, db_port, db_name

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=False)
