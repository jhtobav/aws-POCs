import json


def generate_response(event, status, body, headers={}):

    body = {
        "message": "You have provided a valid Token, you are consuming resources from NORTH VIRGINIA!",
    }

    return {
        "statusCode": status,
        "body": json.dumps(body),
        "headers": headers
    }


def endpoint_consumeResource(event, context):
    return generate_response(event, 200, {"status": True})
