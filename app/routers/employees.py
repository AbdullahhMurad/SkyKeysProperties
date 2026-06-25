from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Employee
from app.schemas.schemas import EmployeeCreate, EmployeeRead

router = APIRouter(prefix="/employees", tags=["Employees"])


# ---------------------------------------------------------------------------
# GET /employees  –  return all employees
# ---------------------------------------------------------------------------
@router.get("/", response_model=List[EmployeeRead])
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(Employee).order_by(Employee.id).all()


# ---------------------------------------------------------------------------
# GET /employees/{id}  –  return a single employee
# ---------------------------------------------------------------------------
@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found.",
        )
    return employee


# ---------------------------------------------------------------------------
# POST /employees  –  create a new employee
# ---------------------------------------------------------------------------
@router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    employee = Employee(**payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
