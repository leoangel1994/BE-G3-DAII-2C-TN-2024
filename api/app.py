from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from boto3.dynamodb.conditions import Key
from datetime import datetime
from mangum import Mangum
from typing import Optional
import boto3

app = FastAPI()

# TODO security: mejorar politicas de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las fuentes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Inicializar el cliente DynamoDB
dynamodb = boto3.resource('dynamodb')
history_table = dynamodb.Table('EventsHistory')

@app.get("/v1/events/history")
def get_event_history(
    sort_by: Optional[str] = Query(None, description="Campo por el que ordenar los eventos (ej: timestamp)"),
    sort_order: Optional[str] = Query("asc", description="Orden de los eventos (asc o desc)"),
    start_date: Optional[str] = Query(None, description="Fecha de inicio en formato YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Fecha de fin en formato YYYY-MM-DD")
):
    try:
        # Filtrar por fechas si se proveen
        filter_expression = None

        if start_date or end_date:
            date_format = "%Y-%m-%d"
            if start_date:
                try:
                    start_datetime = datetime.strptime(start_date, date_format)
                    filter_expression = Key('timestamp').gte(start_datetime.isoformat())
                except ValueError:
                    raise HTTPException(status_code=400, detail="Formato de fecha inválido para start_date")
            
            if end_date:
                try:
                    end_datetime = datetime.strptime(end_date, date_format)
                    if filter_expression:
                        filter_expression = filter_expression & Key('timestamp').lte(end_datetime.isoformat())
                    else:
                        filter_expression = Key('timestamp').lte(end_datetime.isoformat())
                except ValueError:
                    raise HTTPException(status_code=400, detail="Formato de fecha inválido para end_date")

        # Escanear la tabla de eventos con filtro de fechas si existe
        if filter_expression:
            response = history_table.scan(
                FilterExpression=filter_expression
            )
        else:
            response = history_table.scan()

        items = response.get('Items', [])

        # Ordenar los resultados si se solicita
        if sort_by:
            reverse_order = True if sort_order == "desc" else False
            items = sorted(items, key=lambda x: x.get(sort_by, ""), reverse=reverse_order)

        return {"ok": True, "message": "success", "data": {"events": items}}
    
    except Exception as e:
        print(f"Error al obtener el historico de eventos: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener el historico de eventos.")
    
@app.get("/v1/operations/types")
def get_operation_types():
        # TODO: pendiente de definicion de PO   
        return {"ok": True, "message": "success", "data": {"operation-types": ["venta", "reventa"]}}

# adaptar la rest API a Lambda
handler = Mangum(app)