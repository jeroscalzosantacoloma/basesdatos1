from fastapi import APIRouter, HTTPException
import mysql.connector
from typing import List
from models import Grade, GradeCreate
from database import get_connection

router = APIRouter()

@router.post("/grades/", response_model=Grade)
def insert_grade(grade: GradeCreate):
    conn = get_connection()
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
def insert_grades_bulk(grades: List[GradeCreate]):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        INSERT INTO grades (student_id, subject_id, grade)
        VALUES (%s, %s, %s)
        """
        
        grade_data = [(grade.student_id, grade.subject_id, grade.grade) for grade in grades]
        cursor.executemany(query, grade_data)
        conn.commit()

        # Obtener los IDs generados para las calificaciones insertadas
        created_grades = []
        for _ in grades:
            created_grades.append(Grade(id=cursor.lastrowid, **_))

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

@router.get("/grades/", response_model=List[Grade])
def get_grades():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM grades"
        cursor.execute(query)
        results = cursor.fetchall()  # Obtiene todas las calificaciones

        # Convierte los resultados en objetos Grade
        grades = [Grade(id=result['id'], student_id=result['student_id'], subject_id=result['subject_id'], grade=result['grade']) for result in results]
        
        return grades
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        cursor.close()
        conn.close()
