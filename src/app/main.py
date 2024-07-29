import os
import requests
import json
from datetime import datetime
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

DISCORD_PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")

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

    userID = raw_request["member"]["user"]["id"]
    guildID = raw_request["guild_id"]

    # The command being executed
    command_name = data["name"]

    match command_name:
        case "ping":
            send("Pong!", id, token)

def send(message, id, token):
    url = f"https://discord.com/api/interactions/{id}/{token}/callback"

    callback_data = {
        "type": 4,
        "data": {
            "content": message
        }
    }

    response = requests.post(url, json=callback_data)
    
    print("Response status code: ")
    print(response.status_code)

def update(message, token):
    app_id = os.environ.get("ID")

    url = f"https://discord.com/api/webhooks/{app_id}/{token}/messages/@original"

    # JSON data to send with the request
    data = {
        "content": message
    }

    # Send the PATCH request
    response = requests.patch(url, json=data)

    print("Response status code: ")
    print(response.status_code)