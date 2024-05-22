import boto3
from google.cloud import functions_v1

def invoke_aws_lambda(function_name, payload):
    """Invoke an AWS Lambda function."""
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    return json.loads(response['Payload'].read())

def invoke_google_cloud_function(function_name, payload):
    """Invoke a Google Cloud Function."""
    client = functions_v1.CloudFunctionsServiceClient()
    name = f"projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/functions/{function_name}"
    response = client.call_function(name=name, data=json.dumps(payload))
    return json.loads(response.result)
