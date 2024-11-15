from pydantic import BaseModel, Field

class IndustrialEstateResponse(BaseModel):
    siteid: str = Field(alias="siteid")
    sitename: str = Field(alias="sitename")

    class Config:
        from_attributes = True
