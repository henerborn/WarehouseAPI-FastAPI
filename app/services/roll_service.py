from sqlalchemy.orm import Session
from ..models.roll import RollBase
from ..schemas.roll import RollCreate, RollRead

def create_new_roll(db: Session, roll_data: RollCreate):
    db_roll = RollBase(
        length=roll_data.length,
        weight=roll_data.weight
    )
    db.add(db_roll)
    db.commit()
    db.refresh(db_roll)
    return db_roll
