import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    
    try:

        print(event)
        
        parcelamentoTaxas = event['parcelamentoTaxas']
            
        # Calculo de Parcelamento
        parcelaTaxas = Decimal(450 / parcelamentoTaxas)

        return {
            'parcelaTaxas': parcelaTaxas
        }
    
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
