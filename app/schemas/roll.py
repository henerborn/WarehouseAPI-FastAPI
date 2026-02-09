from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class RollSchema(BaseModel):
    length: float
    weight: float

class RollCreate(RollSchema):
    pass

class RollRead(RollSchema):
    id: int
    add_date: datetime
    remove_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class RollUpdate(RollSchema):
    length: Optional[float] = None 
    weight: Optional[float] = None
