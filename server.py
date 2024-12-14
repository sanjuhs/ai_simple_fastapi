import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from contextlib import asynccontextmanager

start_time = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    end_time = time.time()
    print(f"Server startup took {end_time - start_time:.2f} seconds")
    yield
    # Shutdown
    pass

# Initialize FastAPI app
app = FastAPI(
    title="Simple FastAPI Server",
    description="A basic FastAPI implementation with CRUD operations",
    version="1.0.0",
    lifespan=lifespan
)

# Pydantic model for data validation
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

# Simulate a database with a list
items_db = []
current_id = 1

@app.get("/")
async def root():
    print("Root/ base endpoint called")
    return {"message": "Welcome to the FastAPI server!"}

@app.get("/items/", response_model=List[Item])
async def get_items():
    print("get_items endpoint called")
    return items_db

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    print(f"get_item endpoint called with item_id: {item_id}")
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    print("create_item endpoint called")
    global current_id
    item.id = current_id
    current_id += 1
    items_db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    print(f"update_item endpoint called with item_id: {item_id}")
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item.id = item_id
    items_db[item_index] = updated_item
    return updated_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    print(f"delete_item endpoint called with item_id: {item_id}")
    item_index = next((index for index, item in enumerate(items_db) if item.id == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db.pop(item_index)
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
