import json
import boto3

def lambda_handler(event, context):
    
    try:

        print(event)

        client = boto3.resource("dynamodb")
        table = client.Table("EscolaSonhos_Matriculas")
        
        resp = table.get_item(
            Key={
                'id': event['params']['path']['id']
            }
            )
        
        return resp['Item']
    
    except KeyError as e:
        print(f'GOT KeyError: {e}')
        return {
            'statusCode': 404,
            'headers': {},
            'body': json.dumps({'msg': f'KeyError - {e}'})
        }
    except Exception as e:
        print(f'GOT Exception: {e}')
        return {
            'statusCode': 500,
            'headers': {},
            'body': json.dumps({'msg': f'Exception - {e}'})
        }
