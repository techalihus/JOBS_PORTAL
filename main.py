from db import get_db,Base,engine
from schemas import UserCreate,UserResponse,CompanyCreate,CompanyResponse,JobCreate,JobResponse,CreateApplication,ApplicationResponse,LoginRequest,LoginResponse
from fastapi import Depends,FastAPI,HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import List, Optional
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from models import User,Company,Job,JobApplication
import crud


app=FastAPI()

Base.metadata.create_all(bind=engine)

# Register User
@app.post("/User/Register/", response_model=UserResponse)
def User_Create(user: UserCreate, db: Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User Already Added")
    new_user=crud.create_user(db,user)
    return new_user

# Login Users
@app.post("/Login/User/", response_model=LoginResponse)
def Login_user(data: LoginRequest, db: Session=Depends(get_db)):
    user_log=crud.user_login(db,data.email,data.password)
    if not user_log:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    return user_log

# Get User By Email
@app.get("/Users/{email}", response_model=UserResponse )
def User_By_Email(email: str, db: Session=Depends(get_db)):
    user=crud.get_user_by_email(db,email)
    if not user:
         raise HTTPException(status_code=404, detail="Invalid Email")
    return user

# Company Employee Record
@app.post("/Employee/Register/", response_model=CompanyResponse)
def Employee_Record(user: CompanyCreate, db: Session=Depends(get_db)):
    existing_user=db.query(Company).filter(Company.email==user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User Already Added")
    company_employee=crud.create_company(db,user)
    return company_employee

# Update Employee Record
@app.put("/Update/Employee/{company_id}", response_model=CompanyResponse)
def Employee_Record_Update(data: CompanyCreate, company_id: int, db: Session=Depends(get_db), current_user: Company=Depends(crud.get_current_user)):
    user=crud.update_employee_data(db,company_id,data)
    return user

# Delete Employee
@app.delete("/Delete/Employee/{company_id}", response_model=CompanyResponse)
def Delete_Employee(company_id: int, db: Session=Depends(get_db), current_user: Company=Depends(crud.get_current_user)):
    del_emp=crud.delete_employee(db,company_id)
    if not del_emp:
         raise HTTPException(status_code=404, details="Invalid Student_Id")
    return del_emp

# Get All User
@app.get("/Company/Employee/", response_model=List[CompanyResponse])
def All_Employee_Record(db: Session=Depends(get_db), current_user: Company=Depends(crud.get_current_user)):
    return crud.get_all_company_record(db)

# Employee Job
@app.post("/Employee/Job/", response_model=JobResponse)
def Employee_Job(user: JobCreate, db: Session=Depends(get_db) ):
    emp=crud.job_employee(db,user)
    return emp

# Get All Jobs
@app.get("/User/Job/", response_model=List[JobResponse])
def All_Job( db: Session=Depends(get_db), current_user: Company=Depends(crud.get_current_user)):
    return crud.check_job(db)

# Get Employe job By id
@app.get("/User/Get/Id/{company_id}", response_model=JobResponse)
def Job_Id(company_id: int,  db: Session=Depends(get_db), current_user: Company=Depends(crud.get_current_user)):
    user=db.query(Company).filter(Company.id==company_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=" Not Found ")
    job_id=crud.get_job_by_company(db,company_id)
    if not job_id:
        raise HTTPException(status_code=404, detail=" Not Found ")

    return job_id

# Application By Users
@app.post("/User/Application/", response_model=ApplicationResponse)
def User_Application(user: CreateApplication, db: Session=Depends(get_db), current_user: JobApplication=Depends(crud.get_current_user)):
    appli=crud.jobs_application(db,user)
    if not appli:
        raise HTTPException(status_code=403, detail="Not Found")
    return appli

# Get Application By Users
@app.get("/User/Get/Application/{user_id}", response_model=ApplicationResponse)
def Get_Application_By_Id(user_id: int, db: Session=Depends(get_db), current_user: Company=Depends(crud.get_current_user)):
    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=" Not Found ")
    application_id=crud.get_application_id(db,user_id)
    if not application_id:
        raise HTTPException(status_code=404, detail=" Not Found ")

    return application_id

# Get All Application Record
@app.get("/User/All/Application/", response_model=List[ApplicationResponse])
def Application(db: Session=Depends(get_db), current_user: Company=Depends(crud.get_current_user)):
    return crud.check_application(db)















def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )

    # 1. Define Bearer scheme
    schema.setdefault("components", {})["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter *JWT only* from */auth/login*"
        }
    }

    # 2. *CRITICAL*: Apply security to /auth/me
    me_path = schema["paths"].get("/auth/me", {}).get("get")
    if me_path:
        me_path["security"] = [{"bearerAuth": []}]

    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi

