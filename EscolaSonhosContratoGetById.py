import json
import boto3
from decimal import Decimal

def getAlunoMatr(id):
    client = boto3.resource("dynamodb")
    table = client.Table("EscolaSonhos_AlunosMatr")
    alunomatr = table.get_item(
        Key={
            'id': id
        }
    )
    return alunomatr

def getNucleo(idNucleo):
    client = boto3.resource("dynamodb")
    tableNucleos = client.Table("EscolaSonhos_Nucleos")
    nucleo = tableNucleos.get_item(
        Key={
            'id': idNucleo
        }
    )
    return nucleo

def getMatricula(id):
    client = boto3.resource("dynamodb")
    tableMatricula = client.Table("EscolaSonhos_Matriculas")
    matriculas = tableMatricula.get_item(
        Key={
            'id': id
        }
        )
    return matriculas
    
def getAnuidade(idAnuidade):
    client = boto3.resource("dynamodb")
    tableAnuidades = client.Table("EscolaSonhos_Anuidades")
    anuidade = tableAnuidades.get_item(
        Key={
            'id': idAnuidade
        }
    )
    return anuidade

def getValorAnuidade(id):
    
    
    alunomatr = getAlunoMatr(id)
    
    idNucleo = alunomatr['Item']['idNucleo']
    nucleo = getNucleo(idNucleo)
    
    matriculas = getMatricula(id)
    
    idAnuidade = nucleo['Item']['idAnuidade']
    anuidade = getAnuidade(idAnuidade)
        
    valorAnuidade = anuidade['Item']['convencional']['valor']
	
    if alunomatr['Item']['ehFidelidade']:
        valorAnuidade = anuidade['Item']['fidelidade']['valor']
    
    if alunomatr['Item']['temIrmao']:
        valorAnuidade = valorAnuidade - 900
    
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
    
    #valorAnuidadeFinal = valorAnuidade
    
    return valorAnuidade

def lambda_handler(event, context):
    
    try:

        print(event)
        
        descontoValor = 0
        descontoPorcentagem = 0
        parcelamento = 0
        valorAnuidade = 0
        valorAnuidadeFinal = 0
        parcelaAnuidade = 0
        
        parcelamentoTaxas = 0
        parcelaTaxas = 0
        #parcelaFinal = 0
        observacoes = ''
        
        contrato = {}
        temContrato = False
        tituloContrato = 'MATRÍCULA'
        tipoContrato = 0

        client = boto3.resource("dynamodb")
        
        ## Dados Basicos
        tableMatricula = client.Table("EscolaSonhos_Matriculas")
        matriculas = tableMatricula.get_item(
            Key={
                'id': event['params']['path']['id']
            }
            )
            
        print(matriculas['Item'])
        
        
        ## Contrato
        
        tableContratos = client.Table("EscolaSonhos_Contratos")
        contratoRegistro = tableContratos.get_item(
            Key={
                'id': event['params']['path']['id']
            }
            )
            
        try:
            contrato = contratoRegistro['Item']
        except Exception as e:
            print(f'Nao foi encontrado Contrato')
            print(f'Exception: {e}')
        print(contrato)
        
        
        if contrato != {}:
            print('Contrato Cadastrado')
            
            temContrato = True
            
            descontoValor = contrato['desconto']['valor']
            descontoPorcentagem = contrato['desconto']['porcentagem']
            parcelamento = contrato['parcelamento']
            #valorAnuidade = contrato['valorAnuidade']
            valorAnuidadeFinal = contrato['valorAnuidadeFinal']
            parcelaAnuidade = contrato['parcelaAnuidade']
            
            valorAnuidade = getValorAnuidade(event['params']['path']['id'])
            
            parcelamentoTaxas = contrato['parcelamentoTaxas']
            parcelaTaxas = contrato['parcelaTaxas']
            #parcelaFinal = contrato['parcelaFinal']
            
            observacoes = contrato['observacoes']
            
            idNucleo = contrato['idNucleo']
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
                
            tableAlunosMatr = client.Table("EscolaSonhos_AlunosMatr")
            
            alunomatr = tableAlunosMatr.get_item(
                Key={
                    'id': event['params']['path']['id']
                }
                )
                
            if alunomatr['Item']['ehFidelidade']:
                tituloContrato = tituloContrato + ' FIDELIDADE'
                
            #valorAnuidade = anuidade['Item']['convencional']['valor']
            
            termoTaxas = 'Territórios de Aprendizagem'
            if idAnuidade == 'b120ed6c-60bb-48b9-b575-3214203571c1':
                tituloContrato = tituloContrato + ' - NÚCLEO DE EDUCAÇÃO INFANTIL'
            elif idAnuidade == 'b47d909a-58cf-4695-a98c-c50e6414cac6':
                #Transição
                termoTaxas = 'Territórios de Pesquisa'
                tituloContrato = tituloContrato + ' - NÚCLEO DE TRANSIÇÃO'
            elif idAnuidade == '8e31f4b6-e85b-4ee4-a32b-15e829f9089e':
                #Desenvolvimento
                termoTaxas = 'Projetos'
                tituloContrato = tituloContrato + ' - NÚCLEO DE DESENVOLVIMENTO'
            elif idAnuidade == 'b933deda-b5d1-4e1f-a371-ab88cae39976':
                #Aprofundamento-8/9
                termoTaxas = 'Projetos'
                tituloContrato = tituloContrato + ' - NÚCLEO DE APROFUNDAMENTO'
            elif idAnuidade == '93931dde-3154-4e3d-883c-6f33aa3ea159':
                #Aprofundamento-6/7
                termoTaxas = 'Projetos'
                tituloContrato = tituloContrato + ' - NÚCLEO DE APROFUNDAMENTO'
            elif idAnuidade == 'f86dfe61-b53d-4c39-827e-9c781dc5f128':
                #Espansão
                termoTaxas = 'Projeto de Vida'
                tituloContrato = tituloContrato + ' - NÚCLEO DE EXPANSÃO'
                
            tituloContrato = tituloContrato + ' - 2023'
            
            # infantil - fidelidade = 1
            # infantil - convencional = 2
            # transicao - fidelidade = 3
            # transicao - convencional = 4
            # desenvolvimento - fidelidade = 5
            # desenvolvimento - convencional = 6
            # aprofundamento - fidelidade = 7
            # aprofundamento - fidelidade - 6º ano = 8
            # aprofundamento - convencional = 9
            # expansao - fidelidade = 10
            # expansao - convencional = 11
            
            #Infantil
            if idAnuidade == 'b120ed6c-60bb-48b9-b575-3214203571c1':
                if alunomatr['Item']['ehFidelidade']:
                    tipoContrato = 1
                else:
                    tipoContrato = 2
            #Transição
            elif idAnuidade == 'b47d909a-58cf-4695-a98c-c50e6414cac6':
                if alunomatr['Item']['ehFidelidade']:
                    tipoContrato = 3
                else:
                    tipoContrato = 4
            #Desenvolvimento
            elif idAnuidade == '8e31f4b6-e85b-4ee4-a32b-15e829f9089e':
                if alunomatr['Item']['ehFidelidade']:
                    tipoContrato = 5
                else:
                    tipoContrato = 6
            #Aprofundamento-6/7
            elif idAnuidade == '93931dde-3154-4e3d-883c-6f33aa3ea159':
                if alunomatr['Item']['ehFidelidade']:
                    # aprofundamento - fidelidade - 6º ano
                    if nucleo['Item']['idAnuidade'] == 'e8a2a382-c57a-4295-b3e3-b4c2ba5a2255':
                        tipoContrato = 8
                    else:
                        tipoContrato = 7
                else:
                    tipoContrato = 9
            #Aprofundamento-8/9
            elif idAnuidade == 'b933deda-b5d1-4e1f-a371-ab88cae39976':
                if alunomatr['Item']['ehFidelidade']:
                    tipoContrato = 7
                else:
                    tipoContrato = 9
            #Espansão
            elif idAnuidade == 'f86dfe61-b53d-4c39-827e-9c781dc5f128':
                if alunomatr['Item']['ehFidelidade']:
                    tipoContrato = 10
                else:
                    tipoContrato = 11
        
        else :
            print('Contrato NOVO')
        
            table = client.Table("EscolaSonhos_AlunosMatr")
            
            alunomatr = table.get_item(
                Key={
                    'id': event['params']['path']['id']
                }
                )
                
            print(alunomatr['Item'])
                
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
            
            if alunomatr['Item']['ehFidelidade']:
                tituloContrato = tituloContrato + ' FIDELIDADE'
            
            termoTaxas = 'Territórios de Aprendizagem'
            if idAnuidade == 'b120ed6c-60bb-48b9-b575-3214203571c1':
                tituloContrato = tituloContrato + ' - NÚCLEO DE EDUCAÇÃO INFANTIL'
            elif idAnuidade == 'b47d909a-58cf-4695-a98c-c50e6414cac6':
                #Transição
                termoTaxas = 'Territórios de Pesquisa'
                tituloContrato = tituloContrato + ' - NÚCLEO DE TRANSIÇÃO'
            elif idAnuidade == '8e31f4b6-e85b-4ee4-a32b-15e829f9089e':
                #Desenvolvimento
                termoTaxas = 'Projetos'
                tituloContrato = tituloContrato + ' - NÚCLEO DE DESENVOLVIMENTO'
            elif idAnuidade == 'b933deda-b5d1-4e1f-a371-ab88cae39976':
                #Aprofundamento-8/9
                termoTaxas = 'Projetos'
                tituloContrato = tituloContrato + ' - NÚCLEO DE APROFUNDAMENTO'
            elif idAnuidade == '93931dde-3154-4e3d-883c-6f33aa3ea159':
                #Aprofundamento-6/7
                termoTaxas = 'Projetos'
                tituloContrato = tituloContrato + ' - NÚCLEO DE APROFUNDAMENTO'
            elif idAnuidade == 'f86dfe61-b53d-4c39-827e-9c781dc5f128':
                #Espansão
                termoTaxas = 'Projeto de Vida'
                tituloContrato = tituloContrato + ' - NÚCLEO DE EXPANSÃO'
                
            tituloContrato = tituloContrato + ' - 2023'
                
            #Infantil
            if idAnuidade == 'b120ed6c-60bb-48b9-b575-3214203571c1':
                if alunomatr['Item']['ehFidelidade']:
                    tipoContrato = 1
                else:
                    tipoContrato = 2
            #Transição
            elif idAnuidade == 'b47d909a-58cf-4695-a98c-c50e6414cac6':
                if alunomatr['Item']['ehFidelidade']:
                    tipoContrato = 3
                else:
                    tipoContrato = 4
            #Desenvolvimento
            elif idAnuidade == '8e31f4b6-e85b-4ee4-a32b-15e829f9089e':
                if alunomatr['Item']['ehFidelidade']:
                    tipoContrato = 5
                else:
                    tipoContrato = 6
            #Aprofundamento-6/7
            elif idAnuidade == '93931dde-3154-4e3d-883c-6f33aa3ea159':
                if alunomatr['Item']['ehFidelidade']:
                    # aprofundamento - fidelidade - 6º ano
                    if nucleo['Item']['id'] == 'e8a2a382-c57a-4295-b3e3-b4c2ba5a2255':
                        tipoContrato = 8
                    else:
                        tipoContrato = 7
                else:
                    tipoContrato = 9
            #Aprofundamento-8/9
            elif idAnuidade == 'b933deda-b5d1-4e1f-a371-ab88cae39976':
                if alunomatr['Item']['ehFidelidade']:
                    tipoContrato = 7
                else:
                    tipoContrato = 9
            #Espansão
            elif idAnuidade == 'f86dfe61-b53d-4c39-827e-9c781dc5f128':
                if alunomatr['Item']['ehFidelidade']:
                    tipoContrato = 10
                else:
                    tipoContrato = 11
            
            
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
            
            valorAnuidadeFinal = valorAnuidade
            
            # Calculo de Parcelamento
            parcelamento = 12
            parcelaAnuidade = valorAnuidade / parcelamento
            
            parcelamentoTaxas = 12
            parcelaTaxas = 450 / parcelamentoTaxas
            #parcelaFinal = Decimal(parcelaAnuidade) + Decimal(parcelaTaxas)
            
            
            
        
        return {
            'nomeAluno': matriculas['Item']['dadosGerais']['nome'],
            'idNucleo': idNucleo,
            'nomeNucleo': nucleo['Item']['nome'],
            'tituloContrato': tituloContrato,
            'tipoContrato': tipoContrato,
            'valorAnuidade': valorAnuidade,
            'valorTaxas': 450,
            'termoTaxas': termoTaxas,
            'temContrato': temContrato,
            'dadosGerais':{
                'endereco': {
                    'bairro': matriculas['Item']['dadosGerais']['endereco']['bairro'],
                    'cep': matriculas['Item']['dadosGerais']['endereco']['cep'],
                    'numero': matriculas['Item']['dadosGerais']['endereco']['numero'],
                    'rua': matriculas['Item']['dadosGerais']['endereco']['rua']
                }
            },
            'respFinanceiro': {
                'rg': matriculas['Item']['respFinanceiro']['rg'],
                'cpf': matriculas['Item']['respFinanceiro']['cpf'],
                'nome': matriculas['Item']['respFinanceiro']['nome'],
                'dataNascimento': matriculas['Item']['respFinanceiro']['dataNascimento'],
                'contatoPrincipal': matriculas['Item']['respFinanceiro']['contatoPrincipal'],
                'contatoCelular': matriculas['Item']['respFinanceiro']['contatoCelular'],
                'email': matriculas['Item']['respFinanceiro']['email']
             },
            'integral': {
                'opcao': matriculas['Item']['integral']['opcao'],
                'qtdeDias': matriculas['Item']['integral']['qtdeDias']
            },
            'desconto': {
                'valor': descontoValor,
                'porcentagem': descontoPorcentagem
            },
            'parcelamento': parcelamento,
            'valorAnuidadeFinal': valorAnuidadeFinal,
            'parcelaAnuidade': parcelaAnuidade,
            'parcelamentoTaxas': parcelamentoTaxas,
            'parcelaTaxas': parcelaTaxas,
            'observacoes': observacoes
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
