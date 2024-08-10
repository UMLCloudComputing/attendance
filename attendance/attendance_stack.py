from aws_cdk import (
    # Duration,
    Stack,
    Duration,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
)
import os
from constructs import Construct
from dotenv import load_dotenv
load_dotenv()

class AttendanceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_table = dynamodb.TableV2(self, f"Table{construct_id}", partition_key=dynamodb.Attribute(name="userID", type=dynamodb.AttributeType.STRING))
        code_table = dynamodb.TableV2(self, f"Table{construct_id}_Codes", partition_key=dynamodb.Attribute(name="codeID", type=dynamodb.AttributeType.STRING))

        dockerFunc = _lambda.DockerImageFunction(
            scope=self,
            id=f"ID{construct_id}",
            function_name=construct_id,
            environment= {
                "DISCORD_PUBLIC_KEY" : os.getenv('DISCORD_PUBLIC_KEY'),
                "ID" : os.getenv('ID'),
                "AWS_ID" : os.getenv('AWS_ACCESS_KEY_ID'),
                "AWS_KEY" : os.getenv('AWS_SECRET_ACCESS_KEY'),
                "DYNAMO_USERTABLE" : user_table.table_name,
                "DYNAMO_CODETABLE" : code_table.table_name
            },            
            code=_lambda.DockerImageCode.from_image_asset(
                directory="src"
            ),
            timeout=Duration.seconds(300)
        )

        api = apigateway.LambdaRestApi(self, f"API{construct_id}",
            handler=dockerFunc,
            proxy=True,
        )

        user_table.grant_read_write_data(dockerFunc.role)
        code_table.grant_read_write_data(dockerFunc.role)