from datetime import date
from typing import List
from pydantic import BaseModel, Field

class FloodNextThreeDayData(BaseModel):
    siteid: str = Field(alias="siteid")
    sitename: str = Field(alias="sitename")
    water_device_id: str = Field(alias="water_device_id")
    water_device_lat: float = Field(alias="water_device_lat")
    water_device_long: float = Field(alias="water_device_long")
    level_max: float = Field(alias="level_max")
    vol_max: float = Field(alias="vol_max")
    rain_next_3day: float = Field(alias="rain_next_3day")
    rh_min_next_3day: float = Field(alias="rh_min_next_3day")
    rh_max_next_3day: float = Field(alias="rh_max_next_3day")
    rh_mean_next_3day: float = Field(alias="rh_mean_next_3day")
    wd_max_next_3day: float = Field(alias="wd_max_next_3day")
    temp_next_3day: float = Field(alias="temp_next_3day")
    temp_min_next_3day: float = Field(alias="temp_min_next_3day")
    temp_max_next_3day: float = Field(alias="temp_max_next_3day")
    ws_max_next_3day: float = Field(alias="ws_max_next_3day")
    wl_3day_min: float = Field(alias="wl_3day_min")
    wl_3day_max: float = Field(alias="wl_3day_max")
    wl_3day_mean: float = Field(alias="wl_3day_mean")
    wl_vol_3day_min: float = Field(alias="wl_vol_3day_min")
    wl_vol_3day_max: float = Field(alias="wl_vol_3day_max")
    wl_vol_3day_mean: float = Field(alias="wl_vol_3day_mean")
    predict_90_tank: int = Field(alias="predict_90_tank")
    prob_90_tank: float = Field(alias="prob_90_tank")
    predict_95_tank: int = Field(alias="predict_95_tank")
    prob_95_tank: float = Field(alias="prob_95_tank")
    water_warning_level: str = Field(alias="water_warning_level")
    water_warning_order: int = Field(alias="water_warning_order")

    class Config:
        from_attributes = True

class FloodNextThreeDayResponse(BaseModel):
    forecast_date: date = Field(alias="forecast_date")
    forecast_data: List[FloodNextThreeDayData]

    class Config:
        from_attributes = True