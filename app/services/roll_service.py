from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.roll import RollBase
from ..schemas.roll import RollCreate, RollRead, RollUpdate

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

def get_roll_by_id(db: Session, roll_id: int):
    db_roll = db.query(RollBase).get(roll_id)
    if db_roll is None:
        return None
    if db_roll.remove_date:
        return "was_removed"
    return db_roll

def get_roll_by_id_with_removed(db: Session, roll_id: int):
    db_roll = db.query(RollBase).get(roll_id)
    return db_roll

def get_all_rolls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RollBase).filter(RollBase.remove_date == None).offset(skip).limit(limit).all()

def get_all_rolls_with_removed(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RollBase).offset(skip).limit(limit).all()

def update_roll(db: Session, roll_id: int, roll_input: RollUpdate):
    db_roll = db.query(RollBase).get(roll_id)
    if not db_roll:
        return None
    update_data = roll_input.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_roll, field, value)
    
    db.commit()
    db.refresh(db_roll)
    return db_roll

def get_filtered_rolls(
    db: Session,
    id_min: Optional[int] = None, id_max: Optional[int] = None,
    weight_min: Optional[float] = None, weight_max: Optional[float] = None,
    length_min: Optional[float] = None, length_max: Optional[float] = None
):
    query = db.query(RollBase)
    if id_min is not None and id_max is not None:
        query = query.filter(RollBase.id.between(id_min, id_max))

    elif weight_min is not None and weight_max is not None:
        query = query.filter(RollBase.weight.between(weight_min, weight_max))

    elif length_min is not None and length_max is not None:
        query = query.filter(RollBase.length.between(length_min, length_max))
    
    query = query.filter(RollBase.remove_date == None)  # without removed
    
    return query.all() 



    



