import boto3
import os

AWS_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
USER_TABLENAME = os.getenv("DYNAMO_USERTABLE")
CODE_TABLENAME = os.getenv("DYNAMO_CODETABLE")

# TODO: update user attendance stuff

def write_code(code, expiration):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(CODE_TABLENAME)

    response = table.put_item(Item={"codeID": code, "expiration": expiration})

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Item {code} added successfully.")
    else:
        print("Error adding item...")

def get_code_expiration(code):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(CODE_TABLENAME)

    print(code)
    response = table.get_item(Key={"codeID": code})

    expiration = None
    if "Item" in response:
        expiration = response["Item"]["expiration"]

    return expiration

