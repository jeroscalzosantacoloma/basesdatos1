from fastapi import APIRouter, HTTPException
import mysql.connector
from typing import List
from models import Student, StudentCreate  # Asegúrate de importar el nuevo modelo
from database import get_connection

router = APIRouter()

@router.post("/students/", response_model=Student)
def insert_student(student: StudentCreate):
    conn = get_connection()
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

@router.post("/students/bulk/", response_model=List[Student])
def insert_students_bulk(students: List[StudentCreate]):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        INSERT INTO students (code, full_name, emails)
        VALUES (%s, %s, %s)
        """
        
        student_data = [(student.code, student.full_name, student.emails) for student in students]
        cursor.executemany(query, student_data)
        conn.commit()

        created_students = []
        for student in students:
            created_students.append(Student(student_id=cursor.lastrowid, **student.dict()))  

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

@router.get("/students/", response_model=List[Student])
def get_students():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM students"
        cursor.execute(query)
        results = cursor.fetchall()  
        
        students = [
            Student(student_id=result['student_id'], code=result['code'], full_name=result['full_name'], emails=result['emails']) 
            for result in results
        ]
        
        return students
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        cursor.close()
        conn.close()
