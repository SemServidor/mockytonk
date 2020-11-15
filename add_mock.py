import boto3
import uuid
import json


def main(event, context):
    body = json.loads(event["body"])

    if "secretKey" not in body:
        secret_key = str(uuid.uuid4())
    else:
        secret_key = body["secretKey"]

    id = str(uuid.uuid4())

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    stage = event["requestContext"]["stage"]
    table = dynamodb.Table('mockytonk-{}'.format(stage))
    table.put_item(
        Item={
            'id': id,
            'sort': id,
            'secretKey': secret_key,
            'statusCode': body["statusCode"],
            'response': body["response"],
            'headers': body["headers"]
        }
    )

    body = {
        "mockContract": {
            "statusCode": body["statusCode"],
            "response": body["response"],
            "headers": body["headers"]
        },
        "id": id,
        "secretKey": secret_key,
        "url": "https://{}/{}/proxy/{}".format(event["requestContext"]["domainName"], stage, id)
    }
    response = {
        "statusCode": 201,
        "body": json.dumps(body)
    }

    return response
