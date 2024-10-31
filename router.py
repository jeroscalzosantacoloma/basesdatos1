from fastapi import APIRouter, HTTPException
from models import Course, CourseCreate  
from database import get_connection 
from typing import List
import mysql.connector

router = APIRouter()

@router.get("/courses/", response_model=List[Course])
def list_courses():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM courses"
        cursor.execute(query)
        courses = cursor.fetchall()
        return [Course(**course) for course in courses]
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/courses/", response_model=Course)
def insert_course(course: CourseCreate):
    conn = get_connection()  
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        INSERT INTO courses (name, start_date, end_date, teacher_id)
        VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(query, (course.name, course.start_date, course.end_date, course.teacher_id))
        conn.commit()  

        created_course = Course(course_id=cursor.lastrowid, **course.dict())

        return created_course  
    
    except mysql.connector.Error as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        cursor.close()  
        conn.close()

@router.post("/courses/bulk/", response_model=List[Course])
def bulk_insert_courses(courses: List[CourseCreate]):
    conn = get_connection()  
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed.")
        
    cursor = conn.cursor(dictionary=True)  
    try:
        query = """
        INSERT INTO courses (name, start_date, end_date, teacher_id)
        VALUES (%s, %s, %s, %s)
        """
        
        values = [(course.name, course.start_date, course.end_date, course.teacher_id) for course in courses]

        cursor.executemany(query, values)  
        conn.commit()  

        # Para el bulk insert, el último ID generado será el último ID insertado.
        last_id = cursor.lastrowid
        created_courses = [
            Course(course_id=last_id - len(courses) + i + 1, **course.dict())  
            for i, course in enumerate(courses)
        ]

        return created_courses  
    
    except mysql.connector.Error as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        conn.rollback()  
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    finally:
        cursor.close()  
        conn.close()
