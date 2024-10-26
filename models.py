from pydantic import BaseModel, Field

# Modelo para crear un profesor sin incluir teacher_id
class TeacherCreate(BaseModel):
    name: str = Field(..., description="Nombre del docente")  # Nombre del docente
    email: str = Field(..., description="Correo del docente")  # Correo del docente

# Modelo completo del profesor, que incluirá el ID autoincrementable
class Teacher(TeacherCreate):
    teacher_id: int = Field(..., description="ID del docente (autogenerado)")  # ID del docente (autogenerado)



   
