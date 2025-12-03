from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from typing import List

app = FastAPI(title="Student Management System")

# MySQL connection
def get_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root123456',  # Change to your MySQL password
            database='student_db',
            autocommit=False
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Create table if not exists
def init_db():
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                standard INT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()

init_db()

class StudentCreate(BaseModel):
    name: str
    age: int
    standard: int

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Student Management System ",
        "version": "1.0",
        "endpoints": {
            "create_student": "POST /students/",
            "get_students": "GET /students/", 
            "get_by_class": "GET /students/standard/{standard}",
            "update_student": "PUT /students/{student_id}",
            "delete_by_class_name": "DELETE /students/{standard}?student_name=NAME",
            "delete_by_id": "DELETE /students/id/{student_id}"
        }
    }

# CREATE Student
@app.post("/students/")
def create_student(student: StudentCreate):
    if student.standard not in range(1, 11):
        raise HTTPException(status_code=400, detail="Standard must be between 1 and 10")
    
    conn = get_db()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO students (name, age, standard) VALUES (%s, %s, %s)",
        (student.name, student.age, student.standard)
    )
    conn.commit()
    student_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return {"id": student_id, "message": "Student created successfully", "student": student.dict()}

# GET All Students
@app.get("/students/")
def get_all_students():
    conn = get_db()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"students": students}

# GET Students by Class
@app.get("/students/standard/{standard}")
def get_students_by_class(standard: int):
    if standard not in range(1, 11):
        raise HTTPException(status_code=400, detail="Standard must be between 1 and 10")
    
    conn = get_db()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM students WHERE standard = %s", 
        (standard,)
    )
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return {"standard": standard, "students": students}

# UPDATE Student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate):
    if student.standard not in range(1, 11):
        raise HTTPException(status_code=400, detail="Standard must be between 1 and 10")
    
    conn = get_db()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET name = %s, age = %s, standard = %s WHERE id = %s",
        (student.name, student.age, student.standard, student_id)
    )
    conn.commit()
    updated = cursor.rowcount
    cursor.close()
    conn.close()
    
    if updated == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {"message": "Student updated successfully"}

# DELETE Student by CLASS and NAME
@app.delete("/students/{standard}")
def delete_student_by_class_and_name(standard: int, student_name: str = Query(...)):
    if standard not in range(1, 11):
        raise HTTPException(status_code=400, detail="Standard must be between 1 and 10")
    
    conn = get_db()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM students WHERE standard = %s AND name = %s",
        (standard, student_name)
    )
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    conn.close()
    
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Student not found in this class")
    
    return {"message": f"Student {student_name} from Standard {standard} deleted successfully"}

# DELETE Student by ID
@app.delete("/students/id/{student_id}")
def delete_student_by_id(student_id: int):
    conn = get_db()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (student_id,)
    )
    conn.commit()
    deleted = cursor.rowcount
    cursor.close()
    conn.close()
    
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {"message": f"Student with ID {student_id} deleted successfully"}