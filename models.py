from pydantic import Field,BaseModel

class StudentCreate(BaseModel):
    code: str = Field(..., description="Código del estudiante")
    full_name: str = Field(..., description="Nombre completo del estudiante")
    emails: str = Field(..., description="Correo electrónico del estudiante")


class Student(StudentCreate):
    student_id: int = Field(..., description="ID del estudiante (autogenerado)")

    class Config:
        from_attributes = True


