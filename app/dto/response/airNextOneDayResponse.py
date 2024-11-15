from datetime import date
from typing import List
from pydantic import BaseModel, Field

class AirNextOneDayData(BaseModel):
    siteid: str = Field(alias="siteid")
    sitename: str = Field(alias="sitename")
    amphoe: str = Field(alias="amphoe")
    province: str = Field(alias="province")
    air_device_id: str = Field(alias="air_device_id")
    lat_air_device: float = Field(alias="lat_air_device")
    long_air_device: float = Field(alias="long_air_device")
    rain: float = Field(alias="rain")
    rh_min: float = Field(alias="rh_min")
    rh_max: float = Field(alias="rh_max")
    rh_mean: float = Field(alias="rh_mean")
    wd_max: float = Field(alias="wd_max")
    temp: float = Field(alias="temp")
    temp_min: float = Field(alias="temp_min")
    temp_max: float = Field(alias="temp_max")
    ws_max: float = Field(alias="ws_max")
    aqi_predict: float = Field(alias="aqi_predict")

    class Config:
        from_attributes = True

class AirNextOneDayResponse(BaseModel):
    forecast_date: date = Field(alias="forecast_date")
    forecast_data: List[AirNextOneDayData]

    class Config:
        from_attributes = True
