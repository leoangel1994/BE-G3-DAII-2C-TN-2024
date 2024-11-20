import json
import boto3
from datetime import datetime
import uuid

ssm = boto3.client('ssm')

#def get_websocket_url():
#    response = ssm.get_parameter(Name='/eventify-eda-be/websocket-url', WithDecryption=True)
#    return response['Parameter']['Value']

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('ConnectionsTable')
history_table = dynamodb.Table('EventsHistory')

def lambda_handler(event, context):
    
    print(f"Received event: {json.dumps(event)}")

    # Obtener la WebSocket URL
    #websocket_url = get_websocket_url()
    #print(f"La WebSocket URL es: {websocket_url}")

    #url_https = websocket_url.replace("wss://", "https://")

    ws_client = boto3.client('apigatewaymanagementapi',
            endpoint_url="https://edaws.deliver.ar/"#url_https
        )

    try:
        if 'detail' not in event:
            raise KeyError("no se recibio detail en el evento")
        
        detail = event['detail']
        
        if 'operation' not in detail:
            raise KeyError("no se recibio operation en el evento")
        
        operation = detail.get('operation', 'unknown')
        
        if 'source' not in event:
            raise KeyError("no se recibio source en el evento")
        
        source = event.get('source', 'unknown')
        
        if 'detail-type' not in event:
            raise KeyError("no se recibio detail-type en el evento")
        
        detail_type = event.get('detail-type', 'unknown')
        
        # Guardar evento en DynamoDB como historial
        event_id = str(uuid.uuid4())
        item = {
                'eventId': event_id,
                'timestamp': datetime.utcnow().isoformat(),
                'operation': operation,
                'source': source,
                'detail-type': detail_type,
                'detail': detail
            }
        history_table.put_item(
            Item=item
        )

        # Obtener los ConnectionIds almacenados en DynamoDB
        response = table.scan()
        connections = response.get('Items', [])

        for connection in connections:
            connection_id = connection['connectionId']
            print(f"Connection ID: {connection_id}")
            
            # Enviar un mensaje a cada cliente WebSocket usando el API Gateway Management API
            ws_client.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps(item)
            )
    except Exception as e:
        err = f"Error procesando el evento: {str(e)}"
        print(err)
        return {
            'statusCode': 500,
            'body': json.dumps(err)
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Evento processado satisfactoriamente.')
    }
