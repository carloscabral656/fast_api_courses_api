from typing import List, Optional, Any, Dict
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import Path
from fastapi import Query
from fastapi import Response
from fastapi import Header
from models import Course
from time import sleep
from fastapi import Depends
from models import courses_list

from routes import course_router
from routes import user_router

app = FastAPI(
    title="API de Teste", 
    version="0.0.1", 
    description="Uma API para estudo do FastAPI"
)

app.include_router(course_router.router, tags=["courses"])
app.include_router(user_router.router, tags=["users"])

def fake_db():
    try:
        print("Abrindo conexão com o banco de dados")
        sleep(1)
    finally:
        print("Fechando conexão com banco de dados")
        sleep(1)


@app.get("/courses", 
        description="Retorna a lista de todos os cursos", 
        summary="Retorna todos os cursos", 
        response_model=List[Course],
        response_description="Cursos encontrados com sucesso"
)
async def get_courses(db: Any = Depends(fake_db)):
    return courses_list

"""
    End-point que possui parâmetro.
    Passamo entre '{}' e passamos a varável dentro do template.
    O valor é passado como argumento para a função e podemos usar ela dentro da função.
    Esse parâmetro é validado também, então se eu defino como um int, quando eu passar uma letra ele vai devolver um erro.
"""
@app.get("/courses/{course_id}")
async def get_course_by_id(course_id: int = Path(title="ID do curso", description="Deve ser entre 1 e 2", gt=0, lt=3)):
    ## Todo o input do Python é string, então precsiamos fazer o type cast.
    try:
        course = courses_list[course_id]
        return course
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couse not found.")

@app.post("/courses", status_code=status.HTTP_201_CREATED, response_model=Course)
async def create_course(course: Course):
    next_id = len(courses_list) + 1
    course.id = next_id
    courses_list.append(course )
    return course

@app.put("/courses/{course_id}")
async def update_course(course_id: int , course: Course):
    if course_id in courses_list:
        courses_list[course_id] = course
        course.id = course_id
        return course
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couse not found.")
    
@app.delete("/courses/{course_id}")
async def delete_course(course_id: int): 
    if course_id in courses_list:
        del courses_list[course_id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couse not found.")

@app.get("/calculate")
async def calculate(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_geek: str = Header(default=None)):
    print(f'X-GEEK: {x_geek}')
    return a + b

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)