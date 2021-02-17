import json

def seleccionar_numero(event, context):

    numero = event.get('numero')

    body = {
        "message": "Respuesta desde la funcion SELECCIONAR_NUMERO, el numero ingresado es {}".format(numero),
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "numero": int(numero)
    }

    return response