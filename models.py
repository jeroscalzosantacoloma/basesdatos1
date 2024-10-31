from pydantic import BaseModel
from typing import Optional
from datetime import date

class CourseBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    teacher_id: Optional[int]  

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int 
