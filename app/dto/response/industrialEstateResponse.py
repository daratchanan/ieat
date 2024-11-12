from pydantic import BaseModel, Field

class IndustrialEstateResponse(BaseModel):
    siteid: str = Field(alias="sideid")
    sitename: str = Field(alias="sidename")

    class Config:
        orm_mode = True
