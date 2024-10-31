from fastapi import APIRouter, HTTPException
from models import Teacher, TeacherCreate
from database import get_connection 
from typing import List
import mysql.connector

router = APIRouter()

@router.get("/teachers/", response_model=List[Teacher])
def list_teachers():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM teachers"
        cursor.execute(query)
        teachers = cursor.fetchall()
        return [Teacher(**teacher) for teacher in teachers]
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/teachers/", response_model=Teacher)
def insert_teacher(teacher: TeacherCreate):
    conn = get_connection()  
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        INSERT INTO teachers (name, email)
        VALUES (%s, %s)
        """
        
        cursor.execute(query, (teacher.name, teacher.email))
        conn.commit()  

        created_teacher = Teacher(teacher_id=cursor.lastrowid, **teacher.dict())

        return created_teacher  
    
    except mysql.connector.Error as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        cursor.close()  
        conn.close()
@router.post("/teachers/bulk/", response_model=List[Teacher])
def bulk_insert_teachers(teachers: List[TeacherCreate]):
    conn = get_connection()  
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)  
    try:
        query = """
        INSERT INTO teachers (name, email)
        VALUES (%s, %s)
        """
        
        values = [(teacher.name, teacher.email) for teacher in teachers]

        cursor.executemany(query, values)  
        conn.commit()  

        created_teachers = [
            Teacher(teacher_id=cursor.lastrowid + i + 1, **teacher.dict())  
            for i, teacher in enumerate(teachers)
        ]

        return created_teachers  
    
    except mysql.connector.Error as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        cursor.close()  
        conn.close()  

