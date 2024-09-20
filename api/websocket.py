
import json
import boto3

def connect(event, context):

    connection_id = event['requestContext']['connectionId']
    print(f"Conectado client id: {connection_id}")

    return {
        'statusCode': 200,
        'body': json.dumps('Conectado')
    }

def disconnect(event, context):

    connection_id = event['requestContext']['connectionId']
    print(f"Desconectado client id: {connection_id}")
 
    return {
        'statusCode': 200,
        'body': json.dumps('Desconectado')
    }

def default(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        message = body.get('message', 'No message found')

        connection_id = event['requestContext']['connectionId']

        print(f'Mensaje recibido de cliente id ({connection_id}): {message}')

        apig_management_client = boto3.client('apigatewaymanagementapi',
            endpoint_url=f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}"
        )

        # enviar respuesta al cliente WebSocket
        apig_management_client.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps({
                'message': f"Se recibio el mensaje {message}",
                'connectionId': connection_id
            })
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f"Se recibio el mensaje {message}"
            })
        }

    except Exception as e:

        print('error al procesar peticion' + str(e))

        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Internal server error',
                'error': str(e)
            })
        }
