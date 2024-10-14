import json
import boto3

ssm = boto3.client('ssm')

def get_websocket_url():
    response = ssm.get_parameter(Name='/eventify-eda-be/websocket-url', WithDecryption=True)
    return response['Parameter']['Value']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ConnectionsTable')

def lambda_handler(event, context):
    
    print(f"Received event: {json.dumps(event)}")

    # Obtener la WebSocket URL
    websocket_url = get_websocket_url()
    print(f"La WebSocket URL es: {websocket_url}")

    url_https = websocket_url.replace("wss://", "https://")

    ws_client = boto3.client('apigatewaymanagementapi',
            endpoint_url=url_https
        )

    try:
        if 'detail' not in event:
            raise KeyError("no se recibio detail en el evento")
        
        # Validar esquema
        detail = event['detail']

        # Obtener los ConnectionIds almacenados en DynamoDB
        response = table.scan()
        connections = response.get('Items', [])

        for connection in connections:
            connection_id = connection['connectionId']
            print(f"Connection ID: {connection_id}")
            
            # Enviar un mensaje a cada cliente WebSocket usando el API Gateway Management API
            ws_client.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps({
                    'message': f"Evento procesado exitosamente: {detail}"
                })
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
