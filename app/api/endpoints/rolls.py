from typing import List
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.services import roll_service, stats_service
from app.database.session import get_db
from app.schemas.roll import RollCreate, RollRead, RollUpdate, RollStatsResponse
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.post("/", response_model=RollRead)
def add_roll(roll_input: RollCreate, db: Session = Depends(get_db)):
    return roll_service.create_new_roll(db, roll_data=roll_input)

@router.delete("/{roll_id}", response_model=RollRead)
def soft_delete_roll(roll_id: int, db: Session = Depends(get_db)):
    result = roll_service.soft_delete_roll(db, roll_id)
    if result == "not_found":
        raise HTTPException(status_code=404, detail="Roll is not found :(")
    if result == "already_removed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This roll has already been removed earlier"
        )
    return result

@router.delete("/{roll_id}/hard", status_code=status.HTTP_204_NO_CONTENT)
def hard_delete_roll(roll_id: int, db: Session = Depends(get_db)):
    succes = roll_service.hard_delete_roll(db, roll_id)
    if not succes:
        raise HTTPException(status_code=404, detail="Roll is not found for hard remove")

@router.get("/", response_model=List[RollRead])
def get_all_rolls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rolls = roll_service.get_all_rolls(db, skip, limit)
    return rolls

@router.get("/find_all/with_removed", response_model=List[RollRead])
def get_all_rolls_with_removed(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rolls = roll_service.get_all_rolls_with_removed(db, skip, limit)
    return rolls

@router.get("/{roll_id}", response_model=RollRead)
def get_roll_by_id(roll_id: int, db: Session = Depends(get_db)):
    db_roll = roll_service.get_roll_by_id(db, roll_id)
    if db_roll is None:
        raise HTTPException(status_code=404, detail="Roll is not found :(")
    if db_roll == "was_removed":
        raise HTTPException(status_code=410, detail="Roll was removed from warehouse:(")
    return db_roll

@router.get("/{roll_id}/with_removed", response_model=RollRead)
def get_roll_by_id_with_removed(roll_id: int, db: Session = Depends(get_db)):
    db_roll = roll_service.get_roll_by_id_with_removed(db, roll_id)
    if db_roll is None:
        raise HTTPException(status_code=404, detail="Roll is not found :(")
    return db_roll

@router.patch("/{roll_id}", response_model=RollRead)
def update_roll(roll_id: int, roll_input: RollUpdate, db: Session = Depends(get_db)):
    updated_roll = roll_service.update_roll(db, roll_id, roll_input)
    if not updated_roll:
        raise HTTPException(status_code=404, detail="Roll not found :(")
    return updated_roll

@router.get("/", response_model=List[RollRead])
def get_filtered_rolls(
    id_min: Optional[int] = None, id_max: Optional[int] = None,
    weight_min: Optional[float] = None, weight_max: Optional[float] = None,
    length_min: Optional[float] = None, length_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    return roll_service.get_rolls_filtered(
        db, 
        id_min=id_min, id_max=id_max,
        weight_min=weight_min, weight_max=weight_max,
        length_min=length_min, length_max=length_max
    )

@router.get("/stats/summary", response_model=RollStatsResponse)
def get_roll_stats(
    start_date: datetime, 
    end_date: datetime, 
    db: Session = Depends(get_db)
):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    return stats_service.get_stats(db, start_date, end_date)

