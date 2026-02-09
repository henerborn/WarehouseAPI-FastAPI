from sqlalchemy import func
from typing import Optional
from datetime import datetime
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Roll(Base):
    length: Mapped[float] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    add_date: Mapped[datetime] = mapped_column(server_default=func.now())
    remove_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)