from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated, Generic, Optional, TypeVar

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine, func, select

class Campaign(SQLModel, table=True):
    campaign_id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(index=True)
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True,  index=True)

class CreateCampaign(SQLModel):
    name: str
    due_date: datetime | None



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
        if not session.exec(select(Campaign)).first():
            session.add_all([
                Campaign(name="Summer Launch", due_date=datetime.now()),
                Campaign(name="Winter Launch", due_date=datetime.now()),
                Campaign(name="Black Friday", due_date=datetime.now())
            ])
            session.commit()
    yield


app = FastAPI(root_path="/api/v1", lifespan=lifespan)

T = TypeVar("T")
class Response(BaseModel, Generic[T]):
    data: T

@app.get("/")
async def root():
    return {"message":"connection successfull!"}

class PaginatedResponse(SQLModel, Generic[T]):
    data: T
    next: Optional[str]
    prev: Optional[str]
    count: int

@app.get("/campaigns/", response_model=PaginatedResponse[list[Campaign]])
async def read_campaigns(request: Request, session: session_dp, page: int = Query(1, ge=1), page_size: int = Query(10, ge=10, le=30)):
    limit = page_size
    offset= (page -1) * limit
    data = session.exec(select(Campaign).order_by(Campaign.campaign_id).offset(offset).limit(limit)).all()
    base_url = str(request.url).split('?')[0]

    total = session.exec(select(func.count()).select_from(Campaign)).one()

    if offset + limit < total:
        next_url = f"{base_url}?page={page+1}&page_size={limit}"
    else:
        next_url = None

    if page > 1:
        prev_url = f"{base_url}?page={page-1}&page_size={limit}"
    else:
        prev_url = None

    return {
        "next":next_url,
        "prev":prev_url,
        "count":total,
        "data":data
        }

@app.get("/campaigns/{id}", response_model=Response[Campaign])
async def read_campaigns(id: int, session: session_dp):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404)
    return {"data":data}

@app.post("/campaigns/", status_code=201, response_model=Response[Campaign])
async def create_campaign(campaign: CreateCampaign, session: session_dp):
    db_campaign = Campaign.model_validate(campaign)
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return {"data": campaign}

@app.put("/campaign/{id}", response_model=Response[Campaign])
async def update_campaign(id: int, campaign: CreateCampaign, session: session_dp):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404)
    data.name = campaign.name
    data.due_date = campaign.due_date
    session.add(data)
    session.commit()
    session.refresh(data)
    return {"data":data}

@app.delete("/campaign/{id}", status_code=204)
async def delete_campaign(id: int, session: session_dp):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404)
    session.delete(data)
    session.commit()