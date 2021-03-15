import json
import boto3
import os
import hmac
import hashlib
import base64

def sign_up(event, context):
    client = boto3.client('cognito-idp')
    bodyevent = json.loads(str(event.get('body')))

    try:
        resp = client.admin_create_user(
            UserPoolId = bodyevent.get('userpoolid'),
            Username = bodyevent.get('username'),
            UserAttributes=[
                { 'Name': 'name', 'Value': bodyevent.get('name') },
                { 'Name': 'email', 'Value': bodyevent.get('email') },
                { 'Name': 'phone_number', 'Value': bodyevent.get('phone_number') },
            ],
            TemporaryPassword = bodyevent.get('temporaryPassword'),
            MessageAction='SUPPRESS',
            DesiredDeliveryMediums=['SMS']
        )

        resp = client.admin_initiate_auth(
            UserPoolId = bodyevent.get('userpoolid'),
            ClientId = bodyevent.get('clientid'),
            AuthFlow = 'ADMIN_NO_SRP_AUTH',
            AuthParameters = {
                'USERNAME' : bodyevent.get('username'),
                'PASSWORD' : bodyevent.get('temporaryPassword'),
                'SECRET_HASH' : get_secret_hash(bodyevent.get('username'),bodyevent.get('clientid'),bodyevent.get('clientsecret'))
            }
        )

        resp = client.respond_to_auth_challenge(
            ClientId = bodyevent.get('clientid'),
            ChallengeName = 'NEW_PASSWORD_REQUIRED',
            Session = resp['Session'],
            ChallengeResponses={
                'USERNAME' : bodyevent.get('username'),
                'NEW_PASSWORD' : bodyevent.get('password'),
                'SECRET_HASH' : get_secret_hash(bodyevent.get('username'),bodyevent.get('clientid'),bodyevent.get('clientsecret'))
            }
        )

        body = {
            "message": resp['AuthenticationResult']['IdToken']
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        return response

    except client.exceptions.ClientError as e: 
        
        body = {
            "message": e.response['Error']['Message']
        }

        response = {
            "statusCode": e.response['ResponseMetadata']['HTTPStatusCode'],
            "body": json.dumps(body)
        }

        return response

    except Exception as e:
        
        body = {
            "message": str(e)
        }

        response = {
            "statusCode": 500,
            "body": json.dumps(body)
        }

        return response

def get_secret_hash(username, clientid, clientsecret):
    message = username + clientid
    dig = hmac.new(clientsecret.encode('UTF-8'), msg=message.encode('UTF-8'),
                    digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()