import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    
    try:

        print(event)

        client = boto3.resource("dynamodb")
        table = client.Table("EscolaSonhos_AlunosMatr")
        
        alunomatr = table.get_item(
            Key={
                'id': event['id']
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
        
        tableMatricula = client.Table("EscolaSonhos_Matriculas")
        matriculas = tableMatricula.get_item(
            Key={
                'id': event['id']
            }
            )
            
        print(matriculas['Item'])

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
        
        if matriculas['Item']['integral']['opcao']:
            if matriculas['Item']['integral']['qtdeDias'] == 2:
                valorAnuidade = valorIntegral2x
            if matriculas['Item']['integral']['qtdeDias'] == 3:
                valorAnuidade = valorIntegral3x
            if matriculas['Item']['integral']['qtdeDias'] == 5:
                valorAnuidade = valorIntegral
            
        descontoValor = event['desconto']['valor']
        descontoPorcentagem = event['desconto']['porcentagem']
        parcelamento = event['parcelamento']
        
        # Desconto Por Parcelas
        if parcelamento == 1:
            valorAnuidade = valorAnuidade - (valorAnuidade * Decimal(10 / 100))
        elif parcelamento == 2:
            valorAnuidade = valorAnuidade - (valorAnuidade * Decimal(7.5/ 100))
        
        # Desconto Manual
        if descontoValor != 0:
            valorAnuidade = valorAnuidade - Decimal(descontoValor)
        elif descontoPorcentagem != 0:
            valorAnuidade = valorAnuidade - (valorAnuidade * Decimal(descontoPorcentagem/ 100))
            
        # Calculo de Parcelamento
        parcelaAnuidade = Decimal(valorAnuidade / parcelamento)

        return {
            'valorAnuidadeFinal': valorAnuidade,
            'parcelaAnuidade': valorAnuidade / parcelamento
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
