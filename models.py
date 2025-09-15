from typing import Optional
from pydantic import BaseModel, validator

class Course(BaseModel):
    id: Optional[int] = None
    title: str
    clases: int
    hours: int

    @validator('title')
    def validate_title(cls, value):
        words = value.split(" ")
        if(len(words) < 3):
            raise ValueError("The title must have at least 3 words.")
        return value


courses = {
    1: {
        "title": "Programação para Leigos",
        "clases": 112,
        "hours": 58
    },
    2: {
        "title": "Algoritmos e Lógica de Programação",
        "clases": 87,
        "hours": 67
    }
}

courses_list = [Course(id=key, **value) for key, value in courses.items()]