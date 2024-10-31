from pydantic import BaseModel

class StudentCreate(BaseModel):
    code: str
    full_name: str
    emails: str

class Student(StudentCreate):
    student_id: int  


from pydantic import BaseModel, Field
from datetime import date

class Enrollment(BaseModel):
    id: int 
    student_id: int
    course_id: int
    enrollment_date: date


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date
