import json
import boto3
import os
import hmac
import hashlib
import base64


def sign_in_cross_account(event, context):

    try:

        bodyevent = json.loads(str(event.get('body')))

        roles = {
            'us-east-1_jCOnOGPsz': 'local',
            'us-east-1_NsKXmRvr9': 'arn:aws:iam::220228648715:role/externalAuthorization',
            'us-east-1_h6iqBsTk4': 'arn:aws:iam::409044723547:role/externalAuthorization'
        }

        if(roles[bodyevent.get('userpoolid')] == 'local'):
            client = boto3.client('cognito-idp')
        else:
            sts_connection = boto3.client('sts')
            otherAccount = sts_connection.assume_role(
                RoleArn=roles[bodyevent.get('userpoolid')],
                RoleSessionName="externalAuthorization"
            )
            
            ACCESS_KEY = otherAccount['Credentials']['AccessKeyId']
            SECRET_KEY = otherAccount['Credentials']['SecretAccessKey']
            SESSION_TOKEN = otherAccount['Credentials']['SessionToken']

            client = boto3.client(
                'cognito-idp',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                aws_session_token=SESSION_TOKEN,
            )

        resp = client.admin_initiate_auth(
            UserPoolId = bodyevent.get('userpoolid'),
            ClientId = bodyevent.get('clientid'),
            AuthFlow = 'ADMIN_NO_SRP_AUTH',
            AuthParameters = {
                'USERNAME': bodyevent.get('username'),
                'PASSWORD': bodyevent.get('password'),
                'SECRET_HASH': get_secret_hash(bodyevent.get('username'),bodyevent.get('clientid'),bodyevent.get('clientsecret'))
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

    except KeyError as e:
        
        body = {
            "message": "El userpool {} no esta autorizado".format(str(e))
        }

        response = {
            "statusCode": 500,
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