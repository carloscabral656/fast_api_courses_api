from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import Response
from models import Course

app = FastAPI()

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

@app.get("/courses")
async def get_courses():
    return courses

"""
    End-point que possui parâmetro.
    Passamo entre '{}' e passamos a varável dentro do template.
    O valor é passado como argumento para a função e podemos usar ela dentro da função.
    Esse parâmetro é validado também, então se eu defino como um int, quando eu passar uma letra ele vai devolver um erro.
"""
@app.get("/courses/{course_id}")
async def get_course_by_id(course_id: int):
    ## Todo o input do Python é string, então precsiamos fazer o type cast.
    try:
        course = courses[course_id]
        return course
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couse not found.")


@app.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(course: Course):
    next_id = len(courses) + 1
    course.id = next_id
    courses[next_id] = course
    return course


@app.put("/courses/{course_id}")
async def update_course(course_id: int , course: Course):
    if course_id in courses:
        courses[course_id] = course
        course.id = course_id
        return course
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couse not found.")
    
@app.delete("/courses/{course_id}")
async def delete_course(course_id: int): 
    if course_id in courses:
        del courses[course_id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couse not found.")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)