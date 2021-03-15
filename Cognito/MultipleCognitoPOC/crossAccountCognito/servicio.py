import json
import jwt


def servicio(event, context):
    
    token = (event.get('headers')['Authorization']).replace("Bearer ", "")
    userpool = jwt.decode(token, options={"verify_signature": False})['iss']

    body = {
        "message": "you are working whit this cognito:",
        "userpoolID": userpool,
        "token": jwt.decode(token, options={"verify_signature": False})
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Expose-Headers": "Access-Control-Allow-Orign, Access-Control-Allow-Methods"
        }
    }

    return response