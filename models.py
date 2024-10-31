from pydantic import BaseModel

class SubjectBase(BaseModel):
    name: str
    course_id: int

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    subject_id: int

