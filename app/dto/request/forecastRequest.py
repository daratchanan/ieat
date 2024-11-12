from pydantic import BaseModel
from datetime import date

class ForecastRequest(BaseModel):
    sideid: str
    forecast_date: date
