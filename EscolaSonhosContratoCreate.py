import json
import uuid
from datetime import datetime
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    
    try:

        print(event)
        
        observacoes = ''
        try:
            observacoes = event['observacoes']
        except Exception as e:
            print(f'Exception: {e}')
        print(observacoes)
        
        #### Infra
        
        client = boto3.resource("dynamodb")
        table = client.Table("EscolaSonhos_Contratos")
        
        ### Valores
        
        params = {
            'id': event['id'],
            'idNucleo': event['idNucleo'],
            'valorAnuidade': Decimal(str(event['valorAnuidade'])),
            'valorTaxas': Decimal(str(event['valorTaxas'])),
            'integral': {
                'opcao': event['integral']['opcao'],
        		'qtdeDias': event['integral']['qtdeDias']
            },
            'desconto': {
                'valor': Decimal(str(event['desconto']['valor'])),
        		'porcentagem': Decimal(str(event['desconto']['porcentagem']))
            },
            'parcelamento': event['parcelamento'],
            'valorAnuidadeFinal': Decimal(str(event['valorAnuidadeFinal'])),
            'parcelaAnuidade': Decimal(str(event['parcelaAnuidade'])),
            'parcelamentoTaxas': event['parcelamentoTaxas'],
            'parcelaTaxas': Decimal(str(event['parcelaTaxas'])),
            'observacoes': observacoes,
            'ano': 2023
        }
        
        response = table.put_item(
            TableName='EscolaSonhos_Contratos',
            Item=params
        )
        print(response)
        
        return {
            'statusCode': 200,
            'headers': {},
            'body': json.dumps({'msg': 'Contrato realizado com sucesso!', 'id': event['id']})
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
