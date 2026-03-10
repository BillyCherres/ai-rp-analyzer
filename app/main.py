from fastapi import FastAPI
from app.api.routes import health, papers

app = FastAPI()

app.include_router(health.router)
app.include_router(papers.router)