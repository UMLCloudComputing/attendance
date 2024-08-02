import os
import requests
import json
from datetime import datetime
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import secrets

DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")

def generate_code():
    return secrets.randbelow(900000) + 100000

def verify(event):
    signature = event['headers']['x-signature-ed25519']
    timestamp = event['headers']['x-signature-timestamp']

    # validate the interaction

    verify_key = VerifyKey(bytes.fromhex(DISCORD_PUBLIC_KEY))

    message = timestamp + event['body']

    try:
        verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
    except BadSignatureError:
        print("Bad signature")
        return False
    return True


def handler(event, context):
    try:
        # Verify the cryptographic Signature
        if not verify(event):
            return {'statusCode': 401, 'body': json.dumps('Unauthorized')}

        body = json.loads(event['body'])

        if body['type'] == 1:
            return {'statusCode': 200, 'body': json.dumps({'type': 1})}
        else:
            return interact(body)
    except:
        raise

def interact(raw_request):
    data = raw_request["data"]
    token = raw_request["token"]
    id = raw_request["id"]

    # The ID of the user that executed the command
    userID = raw_request["member"]["user"]["id"]

    # The ID of the Guild in which the bot resides in
    guildID = raw_request["guild_id"]

    # A boolean variable that determines if the user who executed the command is an administrator or not
    admin = (int(raw_request["member"]["permissions"]) & 0x8) == 0x8

    # The command being executed
    command_name = data["name"]

    # The parameters of the command
    parameter1 = data["options"][0]["value"]
    parameter2 = data["options"][1]["value"]
    parameter3 = data["options"][2]["value"]
    # The nth parameter is data["options"][n - 1]["value"]


    # You can add new commands by adding new cases to this switch statement
    
    # Send Function: The first parameter can be any string that you want to send back to the user. This is the only thing you need to change.
    # send(message: str, id, token)

    # Update Function: You most likely do not need this function UNLESS you expect the command to last longer than 3 seconds
    # In that case first send a response to the user and then use this function to update the original message
    # The first parameter can be any string that you want to update the original message to. This is the only thing you need to change.
    # update(message: str, token)
    match command_name:
        case "generate":
            if admin: send(f"Attendence Code is {generate_code()} ", id, token)
            else: send("Only administrators can generate attendance codes", id, token)
    
    
# Send a new message
def send(message, id, token):
    url = f"https://discord.com/api/interactions/{id}/{token}/callback"

    callback_data = {
        "type": 4,
        "data": {
            "content": message,
            "flags" : 1 << 6
        }
    }

    response = requests.post(url, json=callback_data)
    
    print("Response status code: ")
    print(response.status_code)

# Updates an already sent message. The flags 1 << 6 means "ephemeral message" which means only the person who sent the command can see the result.
def update(message, token):
    app_id = os.environ.get("ID")

    url = f"https://discord.com/api/webhooks/{app_id}/{token}/messages/@original"

    # JSON data to send with the request
    data = {
        "content": message,
        "flags" : 1 << 6
    }

    # Send the PATCH request
    response = requests.patch(url, json=data)

    print("Response status code: ")
    print(response.status_code)