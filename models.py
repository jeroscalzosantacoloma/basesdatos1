from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# Modelos para Estudiante
class StudentCreate(BaseModel):
    code: str  # Código del estudiante
    full_name: str  # Nombre completo del estudiante
    emails: str  # Correo del estudiante

class Student(StudentCreate):
    student_id: int  # ID del estudiante (autogenerado)

# Modelos para Cursos
class CourseBase(BaseModel):
    name: str  # Nombre del curso
    start_date: date  # Fecha de inicio del curso
    end_date: date  # Fecha de finalización del curso
    teacher_id: Optional[int]  # ID opcional del profesor

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    course_id: int  # ID del curso (autogenerado)

# Modelos para Materias
class SubjectBase(BaseModel):
    name: str  # Nombre de la materia
    course_id: int  # ID del curso asociado a la materia

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    subject_id: int  # ID de la materia (autogenerado)

# Modelos para Calificaciones
class GradeCreate(BaseModel):
    student_id: int  # ID del estudiante
    subject_id: int  # ID de la materia
    grade: float  # Nota del estudiante en la materia

class Grade(BaseModel):
    id: int  # ID autoincrementable
    student_id: int  # ID del estudiante
    subject_id: int  # ID de la materia
    grade: float  # Nota del estudiante

# Modelos para Inscripciones
class Enrollment(BaseModel):
    id: int  # ID autoincrementable de la inscripción
    student_id: int  # ID del estudiante
    course_id: int  # ID del curso
    enrollment_date: date  # Fecha de inscripción

class EnrollmentCreate(BaseModel):
    student_id: int  # ID del estudiante
    course_id: int  # ID del curso
    enrollment_date: date  # Fecha de inscripción

# Modelos para Profesores
class TeacherCreate(BaseModel):
    name: str = Field(..., description="Nombre del docente")  # Nombre del profesor
    email: str = Field(..., description="Correo electrónico del docente")  # Correo del profesor

class Teacher(TeacherCreate):
    teacher_id: int = Field(..., description="ID del docente (autogenerado)")  # ID del profesor (autogenerado)
