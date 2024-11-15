from datetime import date
import re
from typing import List
from pydantic import BaseModel, Field, field_validator

class FirePredictData(BaseModel):
    fcid: str = Field(alias="fcid")
    namethai: str = Field(alias="namethai")
    nameeng: str = Field(alias="nameeng")
    fid: str = Field(alias="fid")
    ieatname: str = Field(alias="ieatname")
    facgroupname: str = Field(alias="facgroupname")
    ieatzone: str = Field(alias="ieatzone")
    factory_age_month: int = Field(alias="factory_age_month")
    predict: int = Field(alias="predict")
    prob: float = Field(alias="prob")
    level: str = Field(alias="level")

    class Config:
        from_attributes = True

class FirePredictResponse(BaseModel):
    year_month: str = Field(alias="year_month")
    fire_predict_data: List[FirePredictData]

    class Config:
        from_attributes = True
