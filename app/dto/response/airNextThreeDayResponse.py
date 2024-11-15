from datetime import date
from typing import List
from pydantic import BaseModel, Field

class AirNextThreeDayData(BaseModel):
    siteid: str = Field(alias="siteid")
    sitename: str = Field(alias="sitename")
    amphoe: str = Field(alias="amphoe")
    province: str = Field(alias="province")
    air_device_id: str = Field(alias="air_device_id")
    lat_air_device: float = Field(alias="lat_air_device")
    long_air_device: float = Field(alias="long_air_device")
    rain_next_3day: float = Field(alias="rain_next_3day")
    rh_min_next_3day: float = Field(alias="rh_min_next_3day")
    rh_max_next_3day: float = Field(alias="rh_max_next_3day")
    rh_mean_next_3day: float = Field(alias="rh_mean_next_3day")
    wd_max_next_3day: float = Field(alias="wd_max_next_3day")
    temp_next_3day: float = Field(alias="temp_next_3day")
    temp_min_next_3day: float = Field(alias="temp_min_next_3day")
    temp_max_next_3day: float = Field(alias="temp_max_next_3day")
    ws_max_next_3day: float = Field(alias="ws_max_next_3day")
    aqi_3day_predict: float = Field(alias="aqi_3day_predict")
    pm25_3day_predict: float = Field(alias="pm25_3day_predict")
    pm10_3day_predict: float = Field(alias="pm10_3day_predict")

    class Config:
        orm_mode = True

class AirNextThreeDayResponse(BaseModel):
    forecast_date: date = Field(alias="forecast_date")
    forecast_data: List[AirNextThreeDayData]
    
    class Config:
        orm_mode = True
