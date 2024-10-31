from pydantic import BaseModel
from datetime import date


class StudentCreate(BaseModel):
    code: str
    full_name: str
    emails: str

class Student(StudentCreate):
    student_id: int

class SubjectBase(BaseModel):
    name: str
    description: str

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    subject_id: int

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date

class Enrollment(BaseModel):
    id: int 
    student_id: int
    course_id: int
    enrollment_date: date
