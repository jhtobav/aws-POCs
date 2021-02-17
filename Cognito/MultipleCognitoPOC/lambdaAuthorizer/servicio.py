import json
import jwt


def servicio(event, context):
    
    token = (event.get('headers')['Authorization']).replace("Bearer ", "")
    userpool = jwt.decode(token, options={"verify_signature": False})['iss']

    body = {
        "message": "you are working whit this cognito:",
        "userpoolID": userpool
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response