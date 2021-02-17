import json

def funcion_tres(event, context):

    body = {
        "message": "Respuesta desde la funcion TRES",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response