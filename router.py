from fastapi import APIRouter, HTTPException
import mysql.connector
from typing import List
from models import Enrollment, EnrollmentCreate  # Asegúrate de tener estos modelos definidos
from database import get_connection

router = APIRouter()

@router.post("/enrollments/", response_model=Enrollment)
def insert_enrollment(enrollment: EnrollmentCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(query, (enrollment.student_id, enrollment.course_id, enrollment.enrollment_date))
        conn.commit()

        # El ID se genera automáticamente en la base de datos
        created_enrollment = Enrollment(id=cursor.lastrowid, **enrollment.dict())
        return created_enrollment
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.post("/enrollments/bulk/", response_model=List[Enrollment])
def insert_enrollments_bulk(enrollments: List[EnrollmentCreate]):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (%s, %s, %s)
        """
        
        # Recopila los datos en una lista de tuplas
        enrollment_data = [(enrollment.student_id, enrollment.course_id, enrollment.enrollment_date) for enrollment in enrollments]
        cursor.executemany(query, enrollment_data)
        conn.commit()

        # Obtener los IDs generados para las inscripciones insertadas
        created_enrollments = []
        for enrollment in enrollments:
            created_enrollments.append(Enrollment(id=cursor.lastrowid, **enrollment.dict()))  # Aquí también, solo el id se obtiene.

        return created_enrollments
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/enrollments/", response_model=List[Enrollment])
def get_enrollments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM enrollments"
        cursor.execute(query)
        results = cursor.fetchall()  # Obtiene todas las inscripciones

        # Convierte los resultados en objetos Enrollment
        enrollments = [
            Enrollment(id=result['id'], student_id=result['student_id'], course_id=result['course_id'], enrollment_date=result['enrollment_date']) 
            for result in results
        ]
        
        return enrollments
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        cursor.close()
        conn.close()


