
import boto3

def getDynamoDBClient(env):
    print("DynamoDB Env: " + env)
    if env == "local":
        return boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    elif env == "prod":
        # return boto3.resource('dynamodb', region_name='us-west-1')
        session = boto3.Session(profile_name='prod')
        return session.resource("dynamodb")
    return None