import json
import boto3

def lambda_handler(event, context):
    
    try:
        
        print(event)
    
        client = boto3.resource("dynamodb")
        
        
        idAluno = event['params']['path']['id']
        print(f'idAluno: {idAluno}')
        
        # Get Aluno
        tableAlunosMatr = client.Table("EscolaSonhos_AlunosMatr")
        alunomatr = tableAlunosMatr.get_item(
            Key={
                'id': idAluno
            }
        )
        
        ehFidelidade = alunomatr['Item']['ehFidelidade']
        
        idNucleo = alunomatr['Item']['idNucleo']
        print(f'idNucleo: {idNucleo}')
        
        # Get Nucleo
        tableNucleos = client.Table("EscolaSonhos_Nucleos")
        nucleo = tableNucleos.get_item(
            Key={
                'id': idNucleo
            }
        )
        
        # Get Anuidade
        idAnuidade = nucleo['Item']['idAnuidade']
        print(f'idAnuidade: {idAnuidade}')
        
        # Download
        idDownload = idAnuidade
        
        # Get Docs
        table = client.Table("EscolaSonhos_DocsDownload")
        lstDocs = table.get_item(
            Key={
                'id': idDownload
            }
        )
        
        result = []
        
        try:
            if ehFidelidade:
                result = table.scan()['Items'][0]['docs']['fidelidade']
            else:
                result = table.scan()['Items'][0]['docs']['convencional']
        except Exception as e:
            print(f'GOT Exception: {e}')
        
        return result
    
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
