import boto3
import json

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
                'Source': 'my.application',
                'DetailType': 'test',
                'Detail': json.dumps({'test_id': '123456', 'status': 'init'}),
                'EventBusName': 'default'
            },
        ]
    )
    print(f"Evento enviado: {response}")

if __name__ == "__main__":
    send_test_event()
