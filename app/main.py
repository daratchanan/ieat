from fastapi import FastAPI
from app.core.database import engine
from app.api import airForecast, factory, fireForecast, industrialEstate

app = FastAPI()

app.include_router(industrialEstate.router)
app.include_router(airForecast.router)
app.include_router(factory.router)
app.include_router(fireForecast.router)

