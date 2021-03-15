import json
import jwt


def servicio_openid(event, context):
    
    print(event)

    token = (event.get('headers')['Authorization']).replace("Bearer ", "")
    userpool = jwt.decode(token, options={"verify_signature": False})['iss']

    body = {
        "message": "you are working whit this cognito:",
        "userpoolID": event.get('headers')
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response