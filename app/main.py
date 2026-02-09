from fastapi import FastAPI
from app.core.config import settings
import uvicorn

app = FastAPI(title=settings.PROJECT_TITLE)

@app.get("/")
def root():
    return {"message": "Hello World"}

# app.include_router()

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)