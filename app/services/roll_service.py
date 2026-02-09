from datetime import datetime
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

# "Hard" delete from database
def hard_delete_roll(db: Session, roll_id: int):
    db_roll = db.query(RollBase).get(roll_id)
    if db_roll:
        db.delete(db_roll)
        db.commit()
        return True
    return False

# "Soft" delete - update remove_date param
def soft_delete_roll(db: Session, roll_id: int):
    db_roll = db.query(RollBase).filter(RollBase.id == roll_id).first()

    if not db_roll:
        return "not_found"
    
    if db_roll.remove_date is not None:
        return "already_removed"
    
    db_roll.remove_date = datetime.now()
    db.commit()
    db.refresh(db_roll)
    return db_roll

def get_all_rolls(db:Session):
    pass

