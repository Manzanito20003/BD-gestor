from fastapi import FastAPI
from Model import DataModel, IndexationModel, TableNameModel

app = FastAPI()


# Endpoints



@app.post("/execute_sql")
async def execute_sql(sql: str):
    try:
        # result= copilador_rodrigo(sql)
        #----
        #parsed_sql = parse_sql(sql)
        #results = execute_action(parsed_sql)
        return {"message": "Query executed successfully", "results": "result"}
    except ValueError as e:
        return {"error": str(e)}



@app.post("/conect_table")
async def connect_table(table_name:TableNameModel):
    print(table_name.table_name)
    # Lógica para conectar a la tabla
    return {"message": "conect_table endpoint is active", "table_name": table_name}




@app.post("/tables_data")
async def tables_data(table_name:TableNameModel):
    print(table_name.table_name)
    # Lógica para conectar a la tabla
    return {"message": "conect_table endpoint is active", "table_name": table_name}


@app.get("/show_schema_info")
async def show_schema_info():
    data={
        "admin": {
            "permisos": {
                "columnas": ["id", "fecha", "cliente", "total"],
                "index": ["id_B++", "total_BRIN"]
            },
            "roles": {
                "columnas": ["id", "fecha", "cliente", "total"],
                "index": ["id_B++", "total_BRIN"]
            },
            "usuarios": {
                "columnas": ["id", "fecha", "cliente", "total"],
                "index": ["id_B++", "total_BRIN"]
            }
        },
        "ventas": {
            "facturas": {
                "columnas": ["id", "fecha", "cliente", "total"],
                "index": ["id_B++", "total_BRIN"]
            },
            "productos": {
                "columnas": ["id", "fecha", "cliente", "total"],
                "index": ["id_B++", "total_BRIN"]
            }
        }
    }

    #

    # Lógica para mostrar las tablas
    return {"message": "show_tables endpoint is active", "data": data}
