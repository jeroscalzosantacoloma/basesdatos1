from fastapi import APIRouter, HTTPException
from models import Student, StudentCreate, Enrollment, EnrollmentCreate, Subject, SubjectCreate
from models import Teacher, TeacherCreate
from models import Course, CourseCreate  
from models import Subject, SubjectCreate 
from models import Grade, GradeCreate
from database import get_connection
from typing import List
import mysql.connector

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
        results = cursor.fetchall()  

        
        grades = [Grade(id=result['id'], student_id=result['student_id'], subject_id=result['subject_id'], grade=result['grade']) for result in results]
        
        return grades
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    finally:
        cursor.close()
        conn.close()






