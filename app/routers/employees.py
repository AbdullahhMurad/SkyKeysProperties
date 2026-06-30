from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin
from app.models.models import AdminUser, Employee
from app.schemas.schemas import EmployeeCreate, EmployeeRead, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["Employees"])


# ---------------------------------------------------------------------------
# GET /employees  –  public, return all employees
# ---------------------------------------------------------------------------
@router.get("/", response_model=List[EmployeeRead])
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(Employee).order_by(Employee.id).all()


# ---------------------------------------------------------------------------
# GET /employees/{id}  –  public, return a single employee
# ---------------------------------------------------------------------------
@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")
    return employee


# ---------------------------------------------------------------------------
# POST /employees  –  admin only
# ---------------------------------------------------------------------------
@router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    employee = Employee(**payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


# ---------------------------------------------------------------------------
# PATCH /employees/{id}  –  admin only
# ---------------------------------------------------------------------------
@router.patch("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee


# ---------------------------------------------------------------------------
# DELETE /employees/{id}  –  admin only
# ---------------------------------------------------------------------------
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin),
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")

    db.delete(employee)
    db.commit()
    return None

# # from typing import List

# # from fastapi import APIRouter, Depends, HTTPException, status
# # from sqlalchemy.orm import Session

# # from app.core.database import get_db
# # from app.models.models import Employee
# # from app.schemas.schemas import EmployeeCreate, EmployeeRead

# # router = APIRouter(prefix="/employees", tags=["Employees"])

# from typing import List

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from app.core.database import get_db
# from app.core.deps import get_current_admin
# from app.models.models import AdminUser, Employee
# from app.schemas.schemas import EmployeeCreate, EmployeeRead, EmployeeUpdate

# router = APIRouter(prefix="/employees", tags=["Employees"])



# # ---------------------------------------------------------------------------
# # GET /employees  –  return all employees
# # ---------------------------------------------------------------------------
# @router.get("/", response_model=List[EmployeeRead])
# def get_all_employees(db: Session = Depends(get_db)):
#     return db.query(Employee).order_by(Employee.id).all()


# # ---------------------------------------------------------------------------
# # GET /employees/{id}  –  return a single employee
# # ---------------------------------------------------------------------------
# @router.get("/{employee_id}", response_model=EmployeeRead)
# def get_employee(employee_id: int, db: Session = Depends(get_db)):
#     employee = db.query(Employee).filter(Employee.id == employee_id).first()
#     if not employee:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Employee with id {employee_id} not found.",
#         )
#     return employee


# # ---------------------------------------------------------------------------
# # POST /employees  –  create a new employee
# # ---------------------------------------------------------------------------
# @router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
# def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
#     employee = Employee(**payload.model_dump())
#     db.add(employee)
#     db.commit()
#     db.refresh(employee)
#     return employee



# # ---------------------------------------------------------------------------
# # POST /employees  –  admin only
# # ---------------------------------------------------------------------------
# @router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
# def create_employee(
#     payload: EmployeeCreate,
#     db: Session = Depends(get_db),
#     current_admin: AdminUser = Depends(get_current_admin),
# ):
#     employee = Employee(**payload.model_dump())
#     db.add(employee)
#     db.commit()
#     db.refresh(employee)
#     return employee


# # ---------------------------------------------------------------------------
# # PATCH /employees/{id}  –  admin only
# # ---------------------------------------------------------------------------
# @router.patch("/{employee_id}", response_model=EmployeeRead)
# def update_employee(
#     employee_id: int,
#     payload: EmployeeUpdate,
#     db: Session = Depends(get_db),
#     current_admin: AdminUser = Depends(get_current_admin),
# ):
#     employee = db.query(Employee).filter(Employee.id == employee_id).first()
#     if not employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")

#     for field, value in payload.model_dump(exclude_unset=True).items():
#         setattr(employee, field, value)

#     db.commit()
#     db.refresh(employee)
#     return employee


# # ---------------------------------------------------------------------------
# # DELETE /employees/{id}  –  admin only
# # ---------------------------------------------------------------------------
# @router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_employee(
#     employee_id: int,
#     db: Session = Depends(get_db),
#     current_admin: AdminUser = Depends(get_current_admin),
# ):
#     employee = db.query(Employee).filter(Employee.id == employee_id).first()
#     if not employee:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")

#     db.delete(employee)
#     db.commit()
#     return None
