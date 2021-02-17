import json

def funcion_uno(event, context):

    body = {
        "message": "Respuesta desde la funcion UNO",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response