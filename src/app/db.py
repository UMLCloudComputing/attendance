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

    response = table.get_item(Key={"codeID": code})

    expiration = None
    if "Item" in response:
        expiration = response["Item"]["expiration"]

    return expiration

def get_user(userid):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(USER_TABLENAME)

    response = table.get_item(Key={"userID": userid})

    data = None
    if "Item" in response:
        data = response["Item"]

    return data

def create_user(userid, attendance_num=0, validation_str=None):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(USER_TABLENAME)

    codes_used = [validation_str] if validation_str != None else []

    response = table.put_item(Item={
        "userID": userid,
        "attendance": attendance_num,
        "codes_used": codes_used
    })

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"User {userid} added successfully.")
    else:
        print(f"Error updating user {userid}...")    

def update_users_attendance(userid, attendance_num, event_validation_str):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(USER_TABLENAME)

    response = table.update_item(
                Key={'userID': userid},
                UpdateExpression="SET codes_used = list_append(codes_used, :val), attendance = :val2",
                ExpressionAttributeValues={":val": [event_validation_str], ":val2": str(attendance_num)}    
                )
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"User {userid} updated successfully.")
    else:
        print(f"Error updating user {userid}...")