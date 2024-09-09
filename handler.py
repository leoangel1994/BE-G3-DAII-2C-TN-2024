import json
from marshmallow import Schema, fields, ValidationError

# validar campos con marshmellow
class TestSchema(Schema):
    test_id = fields.Str(required=True)
    status = fields.Str(required=True)

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    try:
        if 'detail' not in event:
            raise KeyError("Missing 'detail' key in event")

        detail = event['detail']
        schema = TestSchema()
        validated_data = schema.load(detail)

        print(f"Procesando evento test {validated_data['test_id']} con status {validated_data['status']}")

    except KeyError as e:
        print(f"Error procesando el evento: {str(e)}")
    except ValidationError as err:
        print(f"Error de validación de contrato: {err.messages}")
    except Exception as e:
        print(f"Error procesando el evento: {str(e)}")
    return {
        'statusCode': 200,
        'body': json.dumps('Evento processado satisfactoriamente.')
    }
