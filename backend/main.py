from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
import models
import schemas
from typing import List
from sqlalchemy.orm import Session
from PDFUtil import PDF
import json

# from config.celery_utils import create_celery

Base.metadata.create_all(engine)


def create_pdf(todos):
    pdf = PDF()
    pdf.add_page()
    for i in range(0, len(todos)):
        pdf.cell(0, 10, f"ID: {todos[i].id}  TASK: {todos[i].task}", new_x="LMARGIN", new_y="NEXT")
    pdf.output("data_pdf.pdf")


app = FastAPI()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return "todooo"


@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate, session: Session = Depends(get_session)):
    tododb = models.ToDo(task=todo.task)

    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    return tododb


@app.get("/todo/{id}", response_model=schemas.ToDo)
def read_todo(id: int, session: Session = Depends(get_session)):
    todo = session.query(models.ToDo).get(id)

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo


@app.put("/todo/{id}")
def update_todo(id: int, task: str, session: Session = Depends(get_session)):
    todo = session.query(models.ToDo).get(id)
    if todo:
        todo.task = task
        session.commit()

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo with item id {id} not found")

    return todo


@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, session: Session = Depends(get_session)):
    todo = session.query(models.ToDo).get(id)

    if todo:
        session.delete(todo)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return None


@app.get("/todo", response_model=List[schemas.ToDo])
def read_todo_list(session: Session = Depends(get_session)):
    todo_list = session.query(models.ToDo).all()

    create_pdf(todo_list)

    return todo_list