import json
import boto3


def main(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    stage = event["requestContext"]["stage"]
    table = dynamodb.Table('mockytonk-{}'.format(stage))

    print(event["pathParameters"]["proxy"])
    response = table.get_item(Key={'id': event["pathParameters"]["proxy"], 'sort': event["pathParameters"]["proxy"]})
    item = response['Item']

    response = {
        "statusCode": item["statusCode"]
    }
    if "response" in item:
        response["body"] = json.dumps(item["response"])
    if "headers" in item:
        response["headers"] = item["headers"]

    return response
