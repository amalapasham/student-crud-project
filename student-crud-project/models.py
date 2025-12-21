from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Student(Base):
    __tablename__ = "students"
    
    # Student ID (Auto increment)
    id = Column(Integer, primary_key=True, index=True)
    
    # Student Name (Required)
    name = Column(String(100), nullable=False)
    
    # Student Email (Unique, Required)
    email = Column(String(100), unique=True, nullable=False)
    
    # Student Phone Number
    phone = Column(String(20))
    
    # Course Name
    course = Column(String(100))
    
    # Year of Study
    year = Column(Integer)
    
    # Created Time (Auto)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Updated Time (Auto)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())