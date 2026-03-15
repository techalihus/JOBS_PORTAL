from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str]="Users"
    is_active: bool
    created_at: date

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Optional[str]="Users"
    is_active: bool
    created_at: date

    model_config = {
        "from_attributes": True  # <-- replaces orm_mode
    }

class CompanyCreate(BaseModel):
    name: str
    email: EmailStr
    description: str
    is_approved: bool
    created_at: date

class CompanyResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    description: str
    is_approved: bool
    created_at: date

    model_config= {
        "from_attributes" : True

    }

class JobCreate(BaseModel):
    title: str
    description: str
    salary: int
    location: str
    job_type: str
    created_at: date
    company_id: int

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    salary: int
    location: str
    job_type: str
    created_at: date
    company_id: int

    model_config = {
        "from_attributes": True
    }

class CreateApplication(BaseModel):
    user_id: int
    job_id: int
    status: str
    applied_at: date

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    applied_at: date

    model_config = {
        "from_attributes": True
    }

class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str


    model_config = {
        "from_attributes": True  # <-- replaces orm_mode
    }

















