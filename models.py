from pydantic import BaseModel, Field
class GradeCreate(BaseModel):
    student_id: int
    subject_id: int
    grade: float 

# Modelo para la respuesta de datos de la tabla grades (con id)
class Grade(BaseModel):
    id: int  # Este campo será autoincrementable en la base de datos
    student_id: int
    subject_id: int
    grade: float




