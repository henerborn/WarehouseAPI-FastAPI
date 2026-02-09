from sqlalchemy.orm import Session
from app.services import roll_service
from fastapi import APIRouter, Depends
from app.database.session import get_db
from app.schemas.roll import RollCreate, RollRead

router = APIRouter()

@router.post("/", response_model=RollRead)
def add_roll(roll_input: RollCreate, db: Session = Depends(get_db)):
    return roll_service.create_new_roll(db, roll_data=roll_input)

