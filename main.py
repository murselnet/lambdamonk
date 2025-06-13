import sys
sys.path.insert(0, 'paketler')



from fastapi import FastAPI
from typing import Union

app = FastAPI() # Bu 'app' nesnesi Mangum tarafından kullanılacak

@app.get("/")
async def read_root():
    return {"Hello": "World from FastAPI"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: dict):
    return {"item_created": item}










"""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Lambda FastAPI", version="1.0.0")

class User(BaseModel):
    name: str
    email: str

@app.get("/")
async def root():
    return {"message": "FastAPI on Lambda!"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Veritabanı işlemleri
    return {"user_id": user_id, "name": "John"}

@app.post("/users")
async def create_user(user: User):
    # Kullanıcı oluşturma
    return {"message": "User created", "user": user}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
"""