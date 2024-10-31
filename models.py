from pydantic import BaseModel, Field

class TeacherCreate(BaseModel):
    name: str = Field(..., description="Nombre del docente")
    email: str = Field(..., description="Correo electrónico del docente")

class Teacher(TeacherCreate):
    teacher_id: int = Field(..., description="ID del docente (autogenerado)")


