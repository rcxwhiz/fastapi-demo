import json
import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

db_config = json.loads(os.getenv("DB_CONFIG"))
db_url = db_config.pop("url")

engine = create_engine(db_url, **db_config)


def get_db_session():
    with Session(engine) as session:
        yield session


DBSessionDep = Annotated[Session, Depends(get_db_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
