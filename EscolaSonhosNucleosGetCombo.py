import json
import boto3

def lambda_handler(event, context):
    
    client = boto3.resource("dynamodb")
    table = client.Table("EscolaSonhos_Nucleos")
    nucleos = table.scan()['Items']
    
    return nucleos
