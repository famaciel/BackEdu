import json
import boto3

def lambda_handler(event, context):
    
    try:
    
        client = boto3.resource("dynamodb")
        table = client.Table("EscolaSonhos_AlunosMatr")
        
        params = {
            'id': event['params']['path']['id']
        }
        
        response = table.delete_item(
            Key=params
        )
        print(response)
        
        return {
            'statusCode': 200,
            'headers': {},
            'body': json.dumps({'msg': 'AlunosMatr deletado'})
        }
    
    except KeyError as e:
        print(f'GOT KeyError: {e}')
        return {
            'statusCode': 400,
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
