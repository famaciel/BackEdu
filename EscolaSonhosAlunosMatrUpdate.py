import json
import uuid
from datetime import datetime
import boto3

def lambda_handler(event, context):
    
    try:

        print(event)

        client = boto3.resource("dynamodb")
        table = client.Table("EscolaSonhos_AlunosMatr")
        
        # Verifica se o aluno foi criado
        aluno = table.get_item(
            Key={
                #'id': event['id']
                'id': event['params']['path']['id']
            }
            )
        print(aluno['Item'])
        
        # Validação de campos não obrigatórios
        nomeResp02 = ''
        try:
            nomeResp02 = event['body-json']['nomeResp02']
        except KeyError as e:
            print(f'KeyError: {e}')
            
        contatoResp02 = ''
        try:
            contatoResp02 = event['body-json']['contatoResp02']
        except KeyError as e:
            print(f'KeyError: {e}')
    
        
        response = table.update_item(
            Key={
                'id': event['params']['path']['id']
            },
            UpdateExpression="set nome = :p_nome, nomeSearch = :p_nomeSearch, idNucleo = :p_idNucleo, nomeResp01 = :p_nomeResp01, nomeResp01Search= :p_nomeResp01Search, contatoResp01 = :p_contatoResp01, nomeResp02 = :p_nomeResp02, nomeResp02Search = :p_nomeResp02Search, contatoResp02 = :p_contatoResp02, ehFidelidade = :p_ehFidelidade, temIrmao = :p_temIrmao",
            ExpressionAttributeValues={
                ':p_nome': event['body-json']['nome'],
                ':p_nomeSearch': event['body-json']['nome'].casefold(),
                ':p_idNucleo': event['body-json']['idNucleo'],
                ':p_nomeResp01': event['body-json']['nomeResp01'],
                ':p_nomeResp01Search': event['body-json']['nomeResp01'].casefold(),
                ':p_contatoResp01': event['body-json']['contatoResp01'],
                ':p_nomeResp02': nomeResp02,
                ':p_nomeResp02Search': nomeResp02.casefold(),
                ':p_contatoResp02': contatoResp02,
                ':p_ehFidelidade': event['body-json']['ehFidelidade'],
                ':p_temIrmao': event['body-json']['temIrmao']
            },
            ReturnValues="UPDATED_NEW"
        )
        print(response)

        
        return {
            'statusCode': 200,
            'headers': {},
            'body': json.dumps({'msg': 'AlunosMatr atualizado', 'id': event['params']['path']['id']})
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
