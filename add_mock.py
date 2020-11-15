import boto3
import uuid
import json


def main(event, context):
    body = json.loads(event["body"])

    secret_key = get_secret_key(body)
    id = new_id()

    put_item(event, secret_key, id)

    response_body = {
        "mockContract": {
            "statusCode": body["statusCode"],
            "response": body["response"],
            "headers": body["headers"]
        },
        "id": id,
        "secretKey": secret_key,
        "url": get_proxy_url(event, id)
    }
    response = {
        "statusCode": 201,
        "body": json.dumps(response_body)
    }

    return response


def put_item(event, secret_key, id):
    body = json.loads(event["body"])

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


def new_id():
    return str(uuid.uuid4())


def get_secret_key(body):
    if "secretKey" not in body:
        return str(uuid.uuid4())
    return body["secretKey"]


def get_proxy_url(event, id):
    app_context = event["requestContext"]["stage"]
    if app_context == "prod":
        app_context = ""
    else:
        app_context += "/"
    return "https://{}/{}proxy/{}".format(event["requestContext"]["domainName"], app_context, id)
