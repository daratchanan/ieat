from pydantic import BaseModel, Field

class AirNextOneDayResponse(BaseModel):
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
    month: int = Field(alias="month")
    aqi_predict: float = Field(alias="aqi_predict")

    class Config:
        orm_mode = True
