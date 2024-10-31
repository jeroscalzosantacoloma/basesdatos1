from fastapi import APIRouter, HTTPException
import mysql.connector
from typing import List
from models import Student, StudentCreate, Enrollment, EnrollmentCreate  
from database import get_connection

router = APIRouter()

# Manejo de estudiantes
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
        
        enrollment_data = [(enrollment.student_id, enrollment.course_id, enrollment.enrollment_date) for enrollment in enrollments]
        cursor.executemany(query, enrollment_data)
        conn.commit()

        created_enrollments = []
        for enrollment in enrollments:
            created_enrollments.append(Enrollment(id=cursor.lastrowid, **enrollment.dict()))  

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
        results = cursor.fetchall()  

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
