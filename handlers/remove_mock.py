import json
import boto3
from botocore.exceptions import ClientError


def main(event, context):
    print(event["pathParameters"])
    id = event["pathParameters"]["id"]
    secretKey = event["pathParameters"]["secretKey"]

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    stage = event["requestContext"]["stage"]
    table = dynamodb.Table('mockytonk-{}'.format(stage))
    try:
        response = table.delete_item(
            Key={
                'id': id,
                'sort': id
            },
            ConditionExpression="secretKey = :val",
            ExpressionAttributeValues={
                ":val": secretKey
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
            response_body = {
                "errorMessage": e.response['Error']['Message']
            }
            return {
                "statusCode": 400,
                "body": json.dumps(response_body)
            }
        else:
            raise
    else:
        return {
            "statusCode": 204
        }
