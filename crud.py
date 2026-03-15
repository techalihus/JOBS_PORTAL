from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from db import SessionLocal, get_db
import schemas,models
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "myverysecretkey_change_me"
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Login/User/")


# Hash Password
def get_hash_password(password: str):
    return pwd_context.hash(password)

# Verify Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

# Create Token
def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Get Current User From Token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email : str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid auth token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid auth token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# Verify_Admin
def verify_admin(current_user: models.User=Depends(get_current_user)):
    if current_user.role!= "Admin":
        raise HTTPException(status_code=404, detail="Admin Only")
    return current_user
   

# User Create
def create_user(db: Session, user: schemas.UserCreate):
    hash_pass=get_hash_password(user.password)
    create=models.User(name=user.name, email=user.email, password=hash_pass, role=user.role, is_active=user.is_active, created_at=user.created_at)
    db.add(create)
    db.commit()
    db.refresh(create)
    return create

# User Login
def user_login(db: Session, email:str, password:str):
    log=db.query(models.User).filter(models.User.email==email).first()
    if not log:
        raise HTTPException(status_code=404, detail="Not Exits")
    if not verify_password(password, log.password):
        raise HTTPException(status_code=400, detail="Password Incorrect")
    if log.role!= "Admin":
        return {
            "user": log,
            "access_token": None,
            "token_type": None
        }

    token = create_access_token({"sub": log.email})

    return {
        "user": log,
        "access_token": token,
        "token_type": "Bearer"
    }

   

# Get Users 
def get_user_by_email(db: Session, email: str):
    get_user=db.query(models.User).filter(models.User.email==email).first()
    if not get_user:
        raise HTTPException(status_code=404, detail="Invalid Email")
    return get_user
 
# Create Employee Data
def create_company(db: Session, user: schemas.CompanyCreate):
    create_comp=models.Company(name=user.name, email=user.email, description=user.description, is_approved=user.is_approved, created_at=user.created_at)
    db.add(create_comp)
    db.commit()
    db.refresh(create_comp)
    return create_comp

# Update Employee Data
def update_employee_data(db: Session, id: int, user: schemas.CompanyCreate):
    update_emp=db.query(models.Company).filter(models.Company.id==id).first()
    if not update_emp:
        raise HTTPException(status_code=404, detail="ID Does Not Exist")
    update_emp.name=user.name
    update_emp.email=user.email
    update_emp.description=user.description
    update_emp.is_approved=user.is_approved
    update_emp.created_at=user.created_at
    db.commit()
    db.refresh(update_emp)
    return update_emp

# Deleted Employee
def delete_employee(db: Session, id:int):
    delete_emp=db.query(models.Company).filter(models.Company.id==id).first()
    if not delete_emp:
        raise HTTPException(status_code=404, detail="ID Does Not Exist")
    db.delete(delete_emp)
    db.commit()
    return delete_emp

# Get All Compny Employee 
def get_all_company_record(db:Session):
    return db.query(models.Company).all()

# Employee Job
def job_employee(db: Session, user: schemas.JobCreate):
    job_emp=models.Job(title=user.title, description=user.description, salary=user.salary, location=user.location, job_type=user.job_type, created_at=user.created_at, company_id=user.company_id)
    db.add(job_emp)
    db.commit()
    db.refresh(job_emp)
    return job_emp

# Gell All Employee_job
def check_job(db:Session):
    return db.query(models.Job).all()

# Get JOb Employe
def get_job_by_company(db: Session, company_id: int):
    return db.query(models.Job).filter(models.Job.company_id == company_id).first()

    


# Jobs Application  By User
def jobs_application(db: Session, user: schemas.CreateApplication):
    job_app=models.JobApplication(user_id=user.user_id, job_id=user.job_id, status=user.status, applied_at=user.applied_at )
    db.add(job_app)
    db.commit()
    db.refresh(job_app)
    return job_app

# Get Application By Id
def get_application_id(db: Session, user_id: int):
    return db.query(models.JobApplication).filter(models.JobApplication.user_id==user_id).first()

# Check All Job Applications
def check_application(db:Session):
    return db.query(models.JobApplication).all()





    

