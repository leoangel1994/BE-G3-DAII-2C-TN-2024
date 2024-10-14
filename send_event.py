import boto3
import json
from datetime import date

client = boto3.client('events')

session = boto3.Session(
    profile_name='aws-academy',
    region_name='us-east-1' 
)

# Initialize EventBridge client
client = session.client('events')

def send_test_event():
    response = client.put_events(
        Entries=[
            {
                'Source': 'myapp',
                'DetailType': 'test',
                'Detail': json.dumps({
                    "operacion": "venta",
                    "artista": "Monolink",
                    "lugar": "Platea A",
                    "estadio": "Monumental",
                    "fecha_presentacion": "2024-09-29",
                    "fecha_creacion": "2024-09-29",
                    "fecha_actualizacion": "2024-09-29"
                }),
                'EventBusName': 'default'
            }
        ]
    )

    print(f"Evento enviado: {response}")

if __name__ == "__main__":
    send_test_event()
