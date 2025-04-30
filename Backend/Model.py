from pydantic import BaseModel
from typing import Optional


# Modelos de datos para los parámetros de entrada
class DataModel(BaseModel):
    name: str
    description: Optional[str] = None

class IndexationModel(BaseModel):
    table: str
    column: str
    index_type: str
