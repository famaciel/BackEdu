import json
import boto3

def lambda_handler(event, context):
    
    try:

        print(event)

        client = boto3.resource("dynamodb")
        table = client.Table("EscolaSonhos_AlunosMatr")
        
        alunomatr = table.get_item(
            Key={
                'id': event['params']['path']['id']
            }
            )
        
        idNucleo = alunomatr['Item']['idNucleo']
        print(f'idNucleo: {idNucleo}')
            
        tableNucleos = client.Table("EscolaSonhos_Nucleos")
        nucleo = tableNucleos.get_item(
            Key={
                'id': idNucleo
            }
            )
        
        idAnuidade = nucleo['Item']['idAnuidade']
        print(f'idAnuidade: {idAnuidade}')
        
        tableAnuidades = client.Table("EscolaSonhos_Anuidades")
        anuidade = tableAnuidades.get_item(
            Key={
                'id': idAnuidade
            }
            )
            
        valorAnuidade = anuidade['Item']['convencional']['valor']
        
        termoTaxas = 'Territórios de Aprendizagem'
        temAutorizaoSaidaSozinho = False
        
        if idAnuidade == 'b47d909a-58cf-4695-a98c-c50e6414cac6':
            #Transição
            termoTaxas = 'Territórios de Pesquisa'
        elif idAnuidade == '8e31f4b6-e85b-4ee4-a32b-15e829f9089e':
            #Desenvolvimento
            termoTaxas = 'Projetos'
            temAutorizaoSaidaSozinho = True
        elif idAnuidade == 'b933deda-b5d1-4e1f-a371-ab88cae39976':
            #Aprofundamento-8/9
            termoTaxas = 'Projetos'
            temAutorizaoSaidaSozinho = True
        elif idAnuidade == '93931dde-3154-4e3d-883c-6f33aa3ea159':
            #Aprofundamento-6/7
            termoTaxas = 'Projetos'
            temAutorizaoSaidaSozinho = True
        elif idAnuidade == 'f86dfe61-b53d-4c39-827e-9c781dc5f128':
            #Espansão
            termoTaxas = 'Projeto de Vida'
            temAutorizaoSaidaSozinho = True
        
        
        if alunomatr['Item']['ehFidelidade']:
            print('ehFidelidade')
            valorAnuidade = anuidade['Item']['fidelidade']['valor']
            
        if alunomatr['Item']['temIrmao']:
            print('temIrmao')
            valorAnuidade = valorAnuidade - 900
            
        print(f'Valor Anuidade: {valorAnuidade}')
        
        temIntegral = False
        valorIntegral = 0
        valorIntegral2x = 0
        valorIntegral3x = 0
        try:
            if alunomatr['Item']['ehFidelidade']:
                valorIntegral = anuidade['Item']['fidelidade']['integral']
                valorIntegral2x = anuidade['Item']['fidelidade']['integral2x']
                valorIntegral3x = anuidade['Item']['fidelidade']['integral3x']
            else:
                valorIntegral = anuidade['Item']['convencional']['integral']
                valorIntegral2x = anuidade['Item']['convencional']['integral2x']
                valorIntegral3x = anuidade['Item']['convencional']['integral3x']
            
            temIntegral = True
            print(f'Tem Integral')
        except KeyError as e:
            print(f'NÃO Tem Integral')
            
        if alunomatr['Item']['temIrmao'] and temIntegral:
            valorIntegral = valorIntegral - 900
            valorIntegral2x = valorIntegral2x - 900
            valorIntegral3x = valorIntegral3x - 900
        
        return {
            'nomeAluno': alunomatr['Item']['nome'],
            'idNucleo': idNucleo,
            'nomeNucleo': nucleo['Item']['nome'],
            'temAutorizaoSaidaSozinho': temAutorizaoSaidaSozinho,
            'valorAnuidade': valorAnuidade,
            'valorTaxas': 450.,
            'termoTaxas': termoTaxas,
            'temIntegral': temIntegral,
            'valorIntegral': valorIntegral,
            'valorIntegral2x': valorIntegral2x,
            'valorIntegral3x': valorIntegral3x
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
