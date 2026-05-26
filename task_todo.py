from fastapi import FastAPI,HTTPException,status,Query,Depends
from typing import List
from pydantic import BaseModel


app=FastAPI(title="TODO APP")


Todo=[]

class todo(BaseModel):
    title:str
    complted:bool=False


def pagination(
        skip:int=Query(0,ge=0),
        limit:int=Query(10,le=100)
):
    return {
        "skip":skip,
        "limit":limit
    }



@app.post("/todo",status_code=status.HTTP_201_CREATED)
def create_task(task:todo):
    new_todo={
        "id":len(Todo)+1,
        "name":task.title,
        "status":task.complted
    }
    Todo.append(new_todo)
    return {
        "message":"successfully created a new task",
        "todo":new_todo
    }



@app.get("/todo",status_code=status.HTTP_200_OK)
def get_todos(params:dict=Depends(pagination)):
    start=params["skip"]
    end=start+params["limit"]
    return {
        "total":len(Todo),
        "ALL_todo":Todo[start:end]
    }



@app.get("/todo/{id}",status_code=status.HTTP_200_OK)
def get_single_task(todo_id:int):
    for task in Todo:
        if todo_id==task["id"]:
            return task
    raise HTTPException(status_code=404,detail="Not found")    



@app.put("/todo/{id}",status_code=status.HTTP_200_OK)
def update_task(todo_id:int,updated_todo:todo):
    for task in Todo:
        if todo_id==task["id"]:
            return {
                "id":updated_todo.id,
                "title":updated_todo.title,
                "status":updated_todo.complted
            }
    raise HTTPException(status_code=404,detail="Not found")    



@app.delete("/todo/{id}",status_code=status.HTTP_200_OK)
def update_task(todo_id:int):
    for task in Todo:
        if todo_id==task["id"]:
            delted_todo=Todo.pop(todo_id)
        return {
            "message":"successfully deleted",
            "todo_deleted":delted_todo
        }   
    raise HTTPException(status_code=404,detail="Not found")    






            
