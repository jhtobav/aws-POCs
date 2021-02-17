import json

def funcion_dos(event, context):

    body = {
        "message": "Respuesta desde la funcion DOS",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response