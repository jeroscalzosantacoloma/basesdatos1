from fastapi import APIRouter, HTTPException
from models import Grade, GradeCreate 
from database import get_connection 
from typing import List
import mysql.connector

router = APIRouter()

@router.get("/grades/", response_model=List[Grade])
def list_grades():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM grades"
        cursor.execute(query)
        grades = cursor.fetchall()
        return [Grade(**grade) for grade in grades]
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/grades/", response_model=Grade)
def insert_grade(grade: GradeCreate):
    conn = get_connection()  
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        INSERT INTO grades (student_id, subject_id, grade)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(query, (grade.student_id, grade.subject_id, grade.grade))
        conn.commit()  

        # El ID se genera automáticamente en la base de datos
        created_grade = Grade(id=cursor.lastrowid, **grade.dict())

        return created_grade  
    
    except mysql.connector.Error as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        cursor.close()  
        conn.close()

@router.post("/grades/bulk/", response_model=List[Grade])
def bulk_insert_grades(grades: List[GradeCreate]):
    conn = get_connection()  
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)  
    try:
        query = """
        INSERT INTO grades (student_id, subject_id, grade)
        VALUES (%s, %s, %s)
        """
        
        values = [(grade.student_id, grade.subject_id, grade.grade) for grade in grades]

        cursor.executemany(query, values)  
        conn.commit()  

        # Para el bulk insert, el último ID generado será el último ID insertado.
        last_id = cursor.lastrowid
        created_grades = [
            Grade(id=last_id - len(grades) + i + 1, **grade.dict())  
            for i, grade in enumerate(grades)
        ]

        return created_grades  
    
    except mysql.connector.Error as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        cursor.close()  
        conn.close()
