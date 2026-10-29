from pydantic import BaseModel, ConfigDict, Field


class HouseCreate(BaseModel):
    bedrooms: int = Field(ge=0)
    bathrooms: float = Field(ge=0)
    sqft_living: int = Field(gt=0)
    grade: int = Field(ge=1, le=13)
    zipcode: str = Field(min_length=5, max_length=10)

class HouseOut(HouseCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)