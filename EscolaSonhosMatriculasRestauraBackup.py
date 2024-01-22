import json
import uuid
from datetime import datetime
from decimal import Decimal
import boto3

def lambda_handler(event, context):
    
    try:
        
        client = boto3.resource("dynamodb")
        table = client.Table("EscolaSonhos_Matriculas")
        
        f = open('data.json')
        
        data = json.load(f)
        
        print(len(data))
        
        for i in data:
            
            if (i['idNucleo'] == '51eef23e-d0b6-449f-a921-1cf2a98500d3'):
                i['idNucleo'] = 'c8df5bdd-b430-47d3-98e5-851485b72c78'
                
            elif (i['idNucleo'] == 'c8df5bdd-b430-47d3-98e5-851485b72c78'):
                i['idNucleo'] = 'cf909149-ab87-470e-862c-6bc9c58f4881'
                
            elif (i['idNucleo'] == 'cf909149-ab87-470e-862c-6bc9c58f4881'):
                i['idNucleo'] = 'dce3a64e-29e5-4402-9def-3edbf295b496'
                
            elif (i['idNucleo'] == 'dce3a64e-29e5-4402-9def-3edbf295b496'):
                i['idNucleo'] = '69ebb129-90c5-4224-abc8-f3af35f7d988'
                
            elif (i['idNucleo'] == '69ebb129-90c5-4224-abc8-f3af35f7d988'):
                i['idNucleo'] = 'c9daf464-a4ca-4749-9d58-0d8915d858d8'
                
            elif (i['idNucleo'] == 'c9daf464-a4ca-4749-9d58-0d8915d858d8'):
                i['idNucleo'] = '8fd3a800-312a-4fe4-83a1-386faebbb3d9'
                
            elif (i['idNucleo'] == '8fd3a800-312a-4fe4-83a1-386faebbb3d9'):
                i['idNucleo'] = 'a452051a-45e8-4610-9f72-19ef32b57625'
                
            elif (i['idNucleo'] == 'a452051a-45e8-4610-9f72-19ef32b57625'):
                i['idNucleo'] = '145e27cc-0615-4079-b171-24235092e33b'
                
            elif (i['idNucleo'] == '145e27cc-0615-4079-b171-24235092e33b'):
                i['idNucleo'] = 'e8a2a382-c57a-4295-b3e3-b4c2ba5a2255'
                
            elif (i['idNucleo'] == 'e8a2a382-c57a-4295-b3e3-b4c2ba5a2255'):
                i['idNucleo'] = 'c0b7bf05-6ce0-41d3-87e8-c17c978deee5'
                    
            elif (i['idNucleo'] == 'c0b7bf05-6ce0-41d3-87e8-c17c978deee5'):
                i['idNucleo'] = '16d8cca5-4b15-4eac-b962-803522c0f6ed'
                
            elif (i['idNucleo'] == '16d8cca5-4b15-4eac-b962-803522c0f6ed'):
                i['idNucleo'] = '310e25a0-ff64-42b1-accc-4a70d6b0a3f1'
                    
            elif (i['idNucleo'] == '310e25a0-ff64-42b1-accc-4a70d6b0a3f1'):
                i['idNucleo'] = 'eac57ad0-5f00-468e-9c04-e13d8e33406b'
                
            elif (i['idNucleo'] == 'eac57ad0-5f00-468e-9c04-e13d8e33406b'):
                i['idNucleo'] = '631823e5-bdd5-474c-a8b4-0e31a492bd56'
                
            elif (i['idNucleo'] == '631823e5-bdd5-474c-a8b4-0e31a492bd56'):
                i['idNucleo'] = 'dde826da-8535-4edf-ba65-8a3c82d5d18f'
                
            else:
                i['idNucleo'] = ''
                
            response = table.put_item(Item=i)
        
        f.close()

        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
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
    
