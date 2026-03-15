from db import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,DateTime,Text
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String(100), nullable=False)
    email=Column(String(150), nullable=False, unique=True)
    password=Column(String(255), nullable=False)
    role=Column(String(20), nullable=False, default="User")
    is_active=Column(Boolean, default=True)
    created_at=Column(DateTime, default=datetime.utcnow)

    applications=relationship("JobApplication", back_populates="users")

class  Company(Base):
    __tablename__="companies"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String(150), nullable=False)
    email=Column(String(150), nullable=False, unique=True)
    description=Column(Text)
    is_approved=Column(Boolean, default=False)
    created_at=Column(DateTime, default=datetime.utcnow)

    jobs=relationship("Job", back_populates="company")



class Job(Base):
    __tablename__="jobs"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String(150), nullable=False)
    description=Column(Text)
    salary=Column(Integer, nullable=False)
    location=Column(String(100), nullable=False)
    job_type=Column(String(50), nullable=False)
    created_at=Column(DateTime, default=datetime.utcnow)
    company_id=Column(Integer, ForeignKey("companies.id"))

    company=relationship("Company", back_populates="jobs")
    applications=relationship("JobApplication", back_populates="job")

    
    
class JobApplication(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    status = Column(String(50), default="applied") # applied | shortlisted | rejected
    applied_at = Column(DateTime, default=datetime.utcnow)

    users=relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")








