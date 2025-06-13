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


