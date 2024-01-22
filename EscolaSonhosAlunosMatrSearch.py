import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from functools import reduce
from operator import and_

def lambda_handler(event, context):
    
    try:

        print(event)

        client = boto3.resource("dynamodb")
        table = client.Table("EscolaSonhos_AlunosMatr")
        #table = client.Table("EscolaSonhos_Campanha")
        
        idNucleo = ''
        try:
            idNucleo = event['params']['querystring']['idnucleo']
        except KeyError as e:
            print(f'KeyError: {e}')
        print(f'idnucleo == {idNucleo}')
            
        nome = ''
        try:
            nome = event['params']['querystring']['nome'].casefold()
        except KeyError as e:
            print(f'KeyError: {e}')
        print(f'nome == {nome}')
        
        nomeResp = ''
        try:
            nomeResp = event['params']['querystring']['nomeResp'].casefold()
        except KeyError as e:
            print(f'KeyError: {e}')
        print(f'nomeResp == {nomeResp}')
        
        
        if idNucleo and nome and nomeResp:
            print("busca - idNucleo and nome and nomeResp")
            response = table.scan(
                FilterExpression = Attr('idNucleo').eq(idNucleo) & Attr('nomeSearch').contains(nome) & (Attr('nomeResp01Search').contains(nomeResp) | Attr('nomeResp02Search').begins_with(nomeResp))
                )
        elif idNucleo and nome:
            print("busca - idNucleo and nome")
            response = table.scan(
                FilterExpression = Attr('idNucleo').eq(idNucleo) & Attr('nomeSearch').contains(nome)
                )
        elif idNucleo and nomeResp:
            print("busca - idNucleo and nomeResp")
            response = table.scan(
                FilterExpression = Attr('idNucleo').eq(idNucleo) & (Attr('nomeResp01Search').contains(nomeResp) | Attr('nomeResp02Search').contains(nomeResp))
                )
        elif nome and nomeResp:
            print("busca - nome and nomeResp")
            response = table.scan(
                FilterExpression = Attr('nomeSearch').contains(nome) & (Attr('nomeResp01Search').contains(nomeResp) | Attr('nomeResp02Search').contains(nomeResp))
                )
        elif idNucleo:
            print("busca - idNucleo")
            response = table.scan(
                FilterExpression = Attr('idNucleo').eq(idNucleo)
                )
        elif nome:
            print("busca - nome")
            response = table.scan(
                FilterExpression = Attr('nomeSearch').contains(nome)
                )
        elif nomeResp:
            print("busca - nomeResp")
            response = table.scan(
                FilterExpression = Attr('nomeResp01Search').contains(nomeResp) | Attr('nomeResp02Search').contains(nomeResp)
                )
        else:
            print("busca - sem parametros")
            response = table.scan()

        
        return response['Items']
    
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
