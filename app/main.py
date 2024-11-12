from fastapi import FastAPI
from app.core.database import engine
from app.api import airForecast, industrialEstate

app = FastAPI()

app.include_router(airForecast.router)
app.include_router(industrialEstate.router)

