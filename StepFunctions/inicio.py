import json
import boto3

def inicio(event, context):

    client = boto3.client('stepfunctions')

    respuesta = client.start_sync_execution(
        stateMachineArn = 'arn:aws:states:us-east-1:323413004057:stateMachine:HelloWorldExpressStepFunctionsStateMachine-MAMH67pUjivc')

    print(respuesta)

    body = {
        "output": respuesta['output'],
        "outputDetails": respuesta['outputDetails'],
        "name": respuesta['name'],
        "status": respuesta['status']
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
        }