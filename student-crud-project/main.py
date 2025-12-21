from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from database import get_db, engine
from typing import List

# Database tables ni create cheyadam
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student CRUD API - MySQL", version="1.0.0")

# Server health check
@app.get("/")
def root():
    return {"message": "Student CRUD API is running with MySQL Database"}

# ✅ POST - నూతన విద్యార్థిని జోడించండి (Add new student)
@app.post("/students/", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def post(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    # ఈమెయిల్ ఇప్పటికే ఉందో చూడండి
    db_student = db.query(models.Student).filter(models.Student.email == student.email).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# ✅ GET - అన్ని విద్యార్థులను పొందండి (Get all students)
@app.get("/students/", response_model=List[schemas.StudentResponse])
def get(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students

# ✅ GET - ఐడీ ద్వారా ఒక విద్యార్థిని పొందండి (Get student by ID)
@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def get_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# ✅ PUT - విద్యార్థి వివరాలను నవీకరించండి (Update student details)
@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def put(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # ఈమెయిల్ నవీకరిస్తే, అది ఇప్పటికే ఉందో చూడండి
    if student.email and student.email != db_student.email:
        existing = db.query(models.Student).filter(models.Student.email == student.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # ఇవి నవీకరించాలి
    update_data = student.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student

# ✅ DELETE - విద్యార్థిని తొలగించండి (Delete student)
@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    return None

# అదనపు: విద్యార్థులను శోధించండి (Search students - Optional)
@app.get("/students/search/", response_model=List[schemas.StudentResponse])
def search(name: str = None, course: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Student)
    if name:
        query = query.filter(models.Student.name.ilike(f"%{name}%"))
    if course:
        query = query.filter(models.Student.course.ilike(f"%{course}%"))
    return query.all()