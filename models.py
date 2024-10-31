from pydantic import BaseModel

class StudentCreate(BaseModel):
    code: str
    full_name: str
    emails: str

class Student(StudentCreate):
    student_id: int  # Este campo será llenado al crear el estudiante


