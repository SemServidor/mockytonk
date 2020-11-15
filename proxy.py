import json
import boto3


def main(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('mockytonk-dev')

    print(event["pathParameters"]["proxy"])
    response = table.get_item(Key={'id': event["pathParameters"]["proxy"], 'sort': event["pathParameters"]["proxy"]})
    item = response['Item']

    response = {
        "statusCode": item["statusCode"],
        "body": json.dumps(item["response"]),
        "headers": item["headers"]
    }

    return response
