import json
import boto3

USER_POOL_ID = 'us-east-1_HHZ3KrfPj'
USER_POOL_CLIENT_ID = '7esoq4b1cu9l5uuhbgso5gn2a9'


def initiate_authorization(bodyevent):
    client = boto3.client('cognito-idp')
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=USER_POOL_CLIENT_ID,
            AuthFlow='CUSTOM_AUTH',
            AuthParameters={
                'USERNAME': bodyevent.get('username')
            }
        )
    except client.exceptions.NotAuthorizedException as e:
        return None, None, "The username doesn't exists"
    except Exception as e:
        return None, None, str(e)
    return client, resp, "Initiation of authorization succesful"


def respond_challenge(client, resp, bodyevent):
    try:
        resp = client.respond_to_auth_challenge(
            ClientId=USER_POOL_CLIENT_ID,
            ChallengeName="CUSTOM_CHALLENGE",
            Session=resp['Session'],
            ChallengeResponses={
                'USERNAME': bodyevent.get('username'),
                'ANSWER': bodyevent.get('password')
            }
        )
    except client.exceptions.NotAuthorizedException as e:
        return resp, "The username or password is incorrect"
    except Exception as e:
        return resp, str(e)
    return resp, "User is now logged in"


def signIn(bodyevent):

    client, resp, message = initiate_authorization(bodyevent)

    if client is not None:
        return respond_challenge(client, resp, bodyevent)
    else:
        return resp, message


def generate_response(event, status, body, headers={}):
    bodyevent = str(event.get('body'))
    bodyevent = json.loads(bodyevent)

    signin_resp, message = signIn(bodyevent)

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "username": bodyevent.get('username'),
        "password": bodyevent.get('password'),
        "signIn_response": signin_resp,
        "signIn_response_message": message
    }

    return {
        "statusCode": status,
        "body": json.dumps(body),
        "headers": headers
    }


def endpoint_signIn(event, context):
    return generate_response(event, 200, {"status": True})
