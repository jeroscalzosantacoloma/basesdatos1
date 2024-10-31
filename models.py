from pydantic import BaseModel, Field

# Modelo para la respuesta de datos de la tabla grades (con id)
class Grade(BaseModel):
    
    student_id: int
    subject_id: int
    grade: float = Field(..., ge=1.0, le=5.0, description="Grade must be between 1.0 and 5.0")

# Modelo para la creación de un nuevo registro de calificación (sin id)
class GradeCreate(BaseModel):
    student_id: int
    subject_id: int
    grade: float = Field(..., ge=1.0, le=5.0, description="Grade must be between 1.0 and 5.0")
    id: int  # Campo autoincrementable en la base de datos



