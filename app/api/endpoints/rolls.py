from sqlalchemy.orm import Session
from app.services import roll_service
from app.database.session import get_db
from app.schemas.roll import RollCreate, RollRead
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

""" @router.get("/get_rolls")
def get_all_rolls(rolls: RollRead, db: Session):
    pass

@router.get("/get_roll/{roll_id}")
def get_roll_by_id(roll_id: int, rolls: RollRead, db: Session):
    pass """

