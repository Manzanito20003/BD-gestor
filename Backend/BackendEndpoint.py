from fastapi import FastAPI
from Model import DataModel, IndexationModel
app = FastAPI()


# Endpoints

@app.post("/inserccion")
async def insert_data(data: DataModel):
    # Lógica para insertar datos en la base de datos


    return {"message": "Data inserted successfully", "data": data}

@app.delete("/delete/{id}")
async def delete_data(id: int):
    # Lógica para eliminar el recurso con el ID dado
    return {"message": f"Item with id {id} deleted"}

@app.get("/search")
async def search_data(param: str):
    # Lógica para buscar los datos según el parámetro
    return {"result": f"Data for {param}"}

@app.get("/range_search")
async def range_search(begin: int, end: int):
    # Lógica para buscar en un rango
    return {"result": f"Data in range from {begin} to {end}"}

@app.post("/indexation")
async def create_index(index: IndexationModel):
    # Lógica para crear el índice
    return {"message": f"Index created on {index.table}.{index.column} with type {index.index_type}"}

@app.get("/conect")
async def healthcheck():
    # Endpoint para verificar que la API está activa
    return {"message": "API is up and running!"}
