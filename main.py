from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine


# Initialize database
sql_lite_filename = "database.db"
sql_lite_url = f"sqlite:///{sql_lite_filename}"

connect_args = {"check_same_thread":False}
engine = create_engine(sql_lite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

session_dp = Annotated[Session, Depends(get_session)]

# Handles the startup and shutdown of web application 
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(root_path="/api/v1", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message":"connection successfull!"}
