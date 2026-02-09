import uvicorn
from fastapi import FastAPI
from .models.base import Base
from .models.roll import RollBase
from .core.config import settings
from .database.session import engine
from .api.endpoints import rolls


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_TITLE)

app.include_router(rolls.router, prefix="/rolls", tags=["Rolls"])
