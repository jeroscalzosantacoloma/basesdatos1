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
