from pydantic import BaseModel, Field

class FactoryResponse(BaseModel):
    fid: str = Field(alias="fid")
    namethai: str = Field(alias="namethai")
    nameeng: str = Field(alias="nameeng")

    class Config:
        from_attributes = True
