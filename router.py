from fastapi import APIRouter, HTTPException
from models import Subject, SubjectCreate 
from database import get_connection 
from typing import List
import mysql.connector

router = APIRouter()

@router.get("/subjects/", response_model=List[Subject])
def list_subjects():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM subjects"
        cursor.execute(query)
        subjects = cursor.fetchall()
        return [Subject(**subject) for subject in subjects]
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/subjects/", response_model=Subject)
def insert_subject(subject: SubjectCreate):
    conn = get_connection()  
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        INSERT INTO subjects (name, course_id)
        VALUES (%s, %s)
        """
        
        cursor.execute(query, (subject.name, subject.course_id))
        conn.commit()  

        created_subject = Subject(id=cursor.lastrowid, **subject.dict())

        return created_subject  
    
    except mysql.connector.Error as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        cursor.close()  
        conn.close()

@router.post("/subjects/bulk/", response_model=List[Subject])
def bulk_insert_subjects(subjects: List[SubjectCreate]):
    conn = get_connection()  
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)  
    try:
        query = """
        INSERT INTO subjects (name, course_id)
        VALUES (%s, %s)
        """
        
        values = [(subject.name, subject.course_id) for subject in subjects]

        cursor.executemany(query, values)  
        conn.commit()  

        last_id = cursor.lastrowid
        created_subjects = [
            Subject(subject_id=last_id - len(subjects) + i + 1, **subject.dict())  
            for i, subject in enumerate(subjects)
        ]

        return created_subjects  
    
    except mysql.connector.Error as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        cursor.close()  
        conn.close()