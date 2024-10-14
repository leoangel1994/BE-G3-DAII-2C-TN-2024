from fastapi import FastAPI, HTTPException
from mangum import Mangum
import boto3

app = FastAPI()

# Inicializar el cliente DynamoDB
dynamodb = boto3.resource('dynamodb')
history_table = dynamodb.Table('EventsHistory')

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/v1/history")
def get_historico():
    try:
        # Escanear todos los elementos de la tabla de eventos históricos
        response = history_table.scan()
        items = response.get('Items', [])
        
        return {"events": items}
    
    except Exception as e:
        print(f"Error al obtener el historico de eventos: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener el historico de eventos.")

# adaptar la rest API a Lambda
handler = Mangum(app)