import json
import uuid
from datetime import datetime
import boto3

def lambda_handler(event, context):
    
    try:

        print(event)
        
        client = boto3.resource("dynamodb")
        table = client.Table("EscolaSonhos_AlunosMatr")
            
        nomeResp02 = ''
        try:
            nomeResp02 = event['nomeResp02']
        except KeyError as e:
            print(f'KeyError: {e}')
            
        contatoResp02 = ''
        try:
            contatoResp02 = event['contatoResp02']
        except KeyError as e:
            print(f'KeyError: {e}')
    
        params = {
            'id': str(uuid.uuid4()),
            'nome': event['nome'],
            'nomeSearch': event['nome'].casefold(),
            'idNucleo': event['idNucleo'],
            'nomeResp01': event['nomeResp01'],
            'nomeResp01Search': event['nomeResp01'].casefold(),
            'contatoResp01': event['contatoResp01'],
            'nomeResp02': nomeResp02,
            'nomeResp02Search': nomeResp02.casefold(),
            'contatoResp02': contatoResp02,
            'ehFidelidade': event['ehFidelidade'],
            'temIrmao': event['temIrmao'],
            'foiMatriculado': False,
            'ano': 2023,
        }
        
        response = table.put_item(
            TableName='EscolaSonhos_AlunosMatr',
            Item=params
        )
        print(response)
        
        return {
            'statusCode': 201,
            'headers': {},
            'body': json.dumps({'msg': 'AlunosMatr criado', 'id': params['id']})
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
