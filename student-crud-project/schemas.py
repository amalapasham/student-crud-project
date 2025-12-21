from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Student Base Schema (Common fields)
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    course: Optional[str] = None
    year: Optional[int] = None

# Student Create Schema (New student add cheyadaniki)
class StudentCreate(StudentBase):
    pass

# Student Update Schema (Student update cheyadaniki)
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    year: Optional[int] = None

# Student Response Schema (Database nundi response)
class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True