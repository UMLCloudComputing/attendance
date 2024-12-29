import boto3
import os

AWS_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
PARAMETER_NAME = os.getenv("SSM_PARAMETER_NAME")

def set_ssm_parameter(value: str) -> None:
    ssm = boto3.client('ssm')

    ssm.put_parameter(
        Name=PARAMETER_NAME, 
        Value=value, 
        Overwrite=True
    )

def get_ssm_parameter() -> str:
    ssm = boto3.client('ssm')

    response = ssm.get_parameter(Name='/attendance/semester')
    return response['Parameter']['Value']