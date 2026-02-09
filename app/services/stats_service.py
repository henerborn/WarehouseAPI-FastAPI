from typing import Optional
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models.roll import RollBase
from ..schemas.roll import RollCreate, RollRead, RollUpdate

def get_stats(db: Session, start_date: datetime, end_date: datetime):
    # Added and removed rolls for the specified period
    added_count = db.query(RollBase).filter(
        RollBase.add_date.between(start_date, end_date)
    ).count()

    removed_count = db.query(RollBase).filter(
        RollBase.remove_date.between(start_date, end_date)
    ).count()

    # Calculations based on those who were in the warehouse
    on_stock_query = db.query(
        func.avg(RollBase.length).label("avg_l"),
        func.avg(RollBase.weight).label("avg_w"),
        func.max(RollBase.length).label("max_l"),
        func.max(RollBase.weight).label("max_w"),
        func.min(RollBase.length).label("min_l"),
        func.min(RollBase.weight).label("min_w"),
        func.sum(RollBase.weight).label("total_w")
    ).filter(
        RollBase.add_date <= end_date,
        (RollBase.remove_date == None) | (RollBase.remove_date >= start_date)
    ).first()

    """ duration_stats = db.query(
        func.max(RollBase.remove_date - RollBase.add_date),
        func.min(RollBase.remove_date - RollBase.add_date)
    ).filter(
        RollBase.remove_date.between(start_date, end_date)
    ).first() """

    duration_query = db.query(
        RollBase.remove_date, 
        RollBase.add_date
    ).filter(
        RollBase.remove_date.between(start_date, end_date)
    ).all()

    if duration_query:
        durations = [(r.remove_date - r.add_date).total_seconds() for r in duration_query]
        max_duration = max(durations)
        min_duration = min(durations)
    else:
        max_duration = None
        min_duration = None

    return {
        "added_count": added_count,
        "removed_count": removed_count,
        "avg_length": on_stock_query.avg_l,
        "avg_weight": on_stock_query.avg_w,
        "max_length": on_stock_query.max_l,
        "min_length": on_stock_query.min_l,
        "max_weight": on_stock_query.max_w,
        "min_weight": on_stock_query.min_w,
        "total_weight": on_stock_query.total_w,
        "max_duration": max_duration,
        "min_duration": min_duration,
    }





