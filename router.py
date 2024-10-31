from fastapi import APIRouter, HTTPException
from models import Student, StudentCreate
from database import get_connection 
from typing import List
import mysql.connector

router = APIRouter()

@router.get("/students/", response_model=List[Student])
def list_students():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM students"
        cursor.execute(query)
        students = cursor.fetchall()
        return [Student(**student) for student in students]
    except mysql.connector.Error as e:
       
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/students/bulk/", response_model=List[Student])
def bulk_insert_students(students: List[StudentCreate]):
    conn = get_connection()  
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)  
    try:
        
        query = """
        INSERT INTO students (code, full_name, emails)
        VALUES (%s, %s, %s)
        """
        
       
        values = [(student.code, student.full_name, student.emails) for student in students]

        cursor.executemany(query, values)  
        conn.commit()  

       
        created_students = [
            Student(student_id=cursor.lastrowid + i + 1, **student.dict())  
            for i, student in enumerate(students)
        ]

        return created_students  
    
    except mysql.connector.Error as e:
        conn.rollback() 
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        cursor.close() 
        conn.close()   


@router.post("/students/", response_model=Student)
def insert_student(student: StudentCreate):
    conn = get_connection()  
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)  

    try:
        query = """
        INSERT INTO students (code, full_name, emails)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(query, (student.code, student.full_name, student.emails))
        conn.commit()  

        created_student = Student(student_id=cursor.lastrowid, **student.dict())

        return created_student  
    
    except mysql.connector.Error as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        cursor.close()  
        conn.close()    

