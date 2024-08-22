import boto3
import os

AWS_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
USER_TABLENAME = os.getenv("DYNAMO_USERTABLE")
CODE_TABLENAME = os.getenv("DYNAMO_CODETABLE")

def write_code(code, expiration, event_name):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(CODE_TABLENAME)

    response = table.put_item(Item={"codeID": code, "expiration": expiration, "event_name": event_name})

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Item {code} added successfully.")
    else:
        print("Error adding item...")

def get_code(code):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(CODE_TABLENAME)

    response = table.get_item(Key={"codeID": code})

    code = None
    if "Item" in response:
        code = response["Item"]

    return code

def get_user(userid):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(USER_TABLENAME)

    response = table.get_item(Key={"userID": userid})

    data = None
    if "Item" in response:
        data = response["Item"]

    return data

def create_user(userid, attendance_num=0, codes_used=[], events_attended=[]):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(USER_TABLENAME)

    response = table.put_item(Item={
        "userID": userid,
        "attendance": attendance_num,
        "codes_used": codes_used,
        "events_attended": events_attended
    })

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"User {userid} added successfully.")
    else:
        print(f"Error updating user {userid}...")    

def update_user(userid, attendance_num, serialized_code, serialized_event):
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table(USER_TABLENAME)

    response = table.update_item(
                Key={'userID': userid},
                UpdateExpression="SET attendance = :val, codes_used = list_append(codes_used, :val2), events_attended = list_append(events_attended, :val3)",
                ExpressionAttributeValues={
                    ":val": str(attendance_num), 
                    ":val2": [serialized_code], 
                    ":val3": [serialized_event] }    
                )
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"User {userid} updated successfully.")
    else:
        print(f"Error updating user {userid}...")

def reset_user(userid):
    pass