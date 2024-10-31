from pydantic import BaseModel

class StudentBase(BaseModel):
    code: str
    full_name: str
    emails: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    student_id: int