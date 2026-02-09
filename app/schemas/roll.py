from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class RollSchema(BaseModel):
    length: float | None = None 
    weight: float | None = None 

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

class RollStatsResponse(BaseModel):
    added_count: int
    removed_count: int
    avg_length: Optional[float]
    avg_weight: Optional[float]
    max_length: Optional[float]
    min_length: Optional[float]
    max_weight: Optional[float]
    min_weight: Optional[float]
    total_weight: Optional[float]
    max_duration: Optional[float]  # seconds or hours
    min_duration: Optional[float]
