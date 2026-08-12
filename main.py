from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Field, SQLModel, Session, create_engine, select

class Campaign(SQLModel, table=True):
    campaign_id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(index=True)
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime | None = Field(default=lambda: datetime.now(timezone.utc), nullable=True,  index=True)


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
    with Session(engine) as session:
        if not session.exec(select(Campaign.first())):
            session.add_all([
                Campaign(name="Summer Launch", due_date=datetime.now()),
                Campaign(name="Winter Launch", due_date=datetime.now()),
                Campaign(name="Black Friday", due_date=datetime.now())
            ])
    yield

app = FastAPI(root_path="/api/v1", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message":"connection successfull!"}
