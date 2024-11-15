from pydantic import BaseModel
from datetime import date

class ForecastRequest(BaseModel):
    siteid: str
    forecast_date: date
