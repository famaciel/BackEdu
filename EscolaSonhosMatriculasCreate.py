import json
import uuid
from datetime import datetime
import boto3

def lambda_handler(event, context):
    
    try:

        print(event)
        
        #### autorizacoes - Pessoas
        
        autorizacoesPessoa01 = {}
        try:
            autorizacoesPessoa01 = event['autorizacoes'].get('pessoas')[0]
        except Exception as e:
            print(f'Exception: {e}')
        print(autorizacoesPessoa01)
        
        autorizacoesPessoa02 = {}
        try:
            autorizacoesPessoa02 = event['autorizacoes'].get('pessoas')[1]
        except Exception as e:
            print(f'Exception: {e}')
        print(autorizacoesPessoa02)
        
        autorizacoesPessoa03 = {}
        try:
            autorizacoesPessoa03 = event['autorizacoes'].get('pessoas')[2]
        except Exception as e:
            print(f'Exception: {e}')
        print(autorizacoesPessoa03)

        #### seguranca - Pessoas
        
        segurancaPessoa01 = {}
        try:
            segurancaPessoa01 = event['seguranca'].get('pessoas')[0]
        except Exception as e:
            print(f'Exception: {e}')
        print(segurancaPessoa01)
        
        segurancaPessoa02 = {}
        try:
            segurancaPessoa02 = event['seguranca'].get('pessoas')[1]
        except Exception as e:
            print(f'Exception: {e}')
        print(segurancaPessoa02)
        
        segurancaPessoa03 = {}
        try:
            segurancaPessoa03 = event['seguranca'].get('pessoas')[2]
        except Exception as e:
            print(f'Exception: {e}')
        print(segurancaPessoa03)
        
        #### Infra
        
        client = boto3.resource("dynamodb")
        table = client.Table("EscolaSonhos_Matriculas")
            
        #### Parametros
    
        params = {
            'id': event['id'],
            'idNucleo': event['idNucleo'],
            'dadosGerais': {
                'nome': event['dadosGerais']['nome'],
        		'dataNascimento': event['dadosGerais']['dataNascimento'],
        		'sexo': event['dadosGerais']['sexo'],
        		'naturalDe': event['dadosGerais']['naturalDe'],
        		'rg': event['dadosGerais']['rg'] if event['dadosGerais'].get('rg') != None else '',
        		'cpf': event['dadosGerais']['cpf'] if event['dadosGerais'].get('cpf') != None else '',
        		'estado': event['dadosGerais']['estado'],
        		'endereco': {
        			'rua': event['dadosGerais']['endereco']['rua'],
        			'numero': event['dadosGerais']['endereco']['numero'],
        			'bairro': event['dadosGerais']['endereco']['bairro'],
        			'cep': event['dadosGerais']['endereco']['cep'],
        			'contatoResidencial': event['dadosGerais']['endereco']['contatoResidencial'] if event['dadosGerais']['endereco'].get('contatoResidencial') != None else '',
        			'contatoRecado': event['dadosGerais']['endereco']['contatoRecado'] if event['dadosGerais']['endereco'].get('contatoRecado') != None else '',
        		}
            },
            'mae': {
        		'nome': event['mae']['nome'] if event['mae'].get('nome') != None else '',
        		'dataNascimento': event['mae']['dataNascimento'] if event['mae'].get('dataNascimento') != None else '',
        		'rg': event['mae']['rg'] if event['mae'].get('rg') != None else '',
        		'cpf': event['mae']['cpf'] if event['mae'].get('cpf') != None else '',
        		'profissao': event['mae']['profissao'] if event['mae'].get('profissao') != None else '',
        		'localTrabalho': event['mae']['localTrabalho'] if event['mae'].get('localTrabalho') != None else '',
        		'cargo': event['mae']['cargo'] if event['mae'].get('cargo') != None else '',
        		'contatoPrincipal': event['mae']['contatoPrincipal'] if event['mae'].get('contatoPrincipal') != None else '',
        		'contatoCelular': event['mae']['contatoCelular'] if event['mae'].get('contatoCelular') != None else '',
        		'email': event['mae']['email'] if event['mae'].get('email') != None else ''
        	},
        	'pai': {
        		'nome': event['pai']['nome'] if event['pai'].get('nome') != None else '',
        		'dataNascimento': event['pai']['dataNascimento'] if event['pai'].get('dataNascimento') != None else '',
        		'rg': event['pai']['rg'] if event['pai'].get('rg') != None else '',
        		'cpf': event['pai']['cpf'] if event['pai'].get('cpf') != None else '',
        		'profissao': event['pai']['profissao'] if event['pai'].get('profissao') != None else '',
        		'localTrabalho': event['pai']['localTrabalho'] if event['pai'].get('localTrabalho') != None else '',
        		'cargo': event['pai']['cargo'] if event['pai'].get('cargo') != None else '',
        		'contatoPrincipal': event['pai']['contatoPrincipal'] if event['pai'].get('contatoPrincipal') != None else '',
        		'contatoCelular': event['pai']['contatoCelular'] if event['pai'].get('contatoCelular') != None else '',
        		'email': event['pai']['email'] if event['pai'].get('email') != None else ''
        	},
        	'respFinanceiro': {
        		'nome': event['respFinanceiro']['nome'] if event['respFinanceiro'].get('nome') != None else '',
        		'dataNascimento': event['respFinanceiro']['dataNascimento'] if event['respFinanceiro'].get('dataNascimento') != None else '',
        		'rg': event['respFinanceiro']['rg'] if event['respFinanceiro'].get('rg') != None else '',
        		'cpf': event['respFinanceiro']['cpf'] if event['respFinanceiro'].get('cpf') != None else '',
        		'profissao': event['respFinanceiro']['profissao'] if event['respFinanceiro'].get('profissao') != None else '',
        		'localTrabalho': event['respFinanceiro']['localTrabalho'] if event['respFinanceiro'].get('localTrabalho') != None else '',
        		'cargo': event['respFinanceiro']['cargo'] if event['respFinanceiro'].get('cargo') != None else '',
        		'contatoPrincipal': event['respFinanceiro']['contatoPrincipal'] if event['respFinanceiro'].get('contatoPrincipal') != None else '',
        		'contatoCelular': event['respFinanceiro']['contatoCelular'] if event['respFinanceiro'].get('contatoCelular') != None else '',
        		'email': event['respFinanceiro']['email'] if event['respFinanceiro'].get('email') != None else ''
        	},
        	'autorizacoes': {
        		'tipoSanguineo': event['autorizacoes']['tipoSanguineo'] if event['autorizacoes'].get('tipoSanguineo') != None else '',
        		'alergias': event['autorizacoes']['alergias'] if event['autorizacoes'].get('alergias') != None else '',
        		'restricaoAlimentar': event['autorizacoes']['restricaoAlimentar'] if event['autorizacoes'].get('restricaoAlimentar') != None else '',
        		'medicamentosUsoContinuo': event['autorizacoes']['medicamentosUsoContinuo'] if event['autorizacoes'].get('medicamentosUsoContinuo') != None else '',
        		'observacoes': event['autorizacoes']['observacoes'] if event['autorizacoes'].get('observacoes') != None else '',
        		'pessoas': [
        			{
        				'nome': autorizacoesPessoa01['nome'] if autorizacoesPessoa01.get('nome') != None else '',
        				'contato': autorizacoesPessoa01['contato'] if autorizacoesPessoa01.get('contato') != None else ''
        			},
        			{
        				'nome': autorizacoesPessoa02['nome'] if autorizacoesPessoa02.get('nome') != None else '',
        				'contato': autorizacoesPessoa02['contato'] if autorizacoesPessoa02.get('contato') != None else ''
        			},
        			{
        				'nome': autorizacoesPessoa03['nome'] if autorizacoesPessoa03.get('nome') != None else '',
        				'contato': autorizacoesPessoa03['contato'] if autorizacoesPessoa03.get('contato') != None else ''
        			}
        		],
        	},
        	'seguranca': {
        		'observacoes': event['seguranca']['observacoes'] if event['seguranca'].get('observacoes') != None else '',
        		'pessoas': [
        			{
        				'nome': segurancaPessoa01['nome'] if segurancaPessoa01.get('nome') != None else '',
        				'parentesco': segurancaPessoa01['parentesco'] if segurancaPessoa01.get('parentesco') != None else ''
        			},
        			{
        				'nome': segurancaPessoa02['nome'] if segurancaPessoa02.get('nome') != None else '',
        				'parentesco': segurancaPessoa02['parentesco'] if segurancaPessoa02.get('parentesco') != None else ''
        			},
        			{
        				'nome': segurancaPessoa03['nome'] if segurancaPessoa03.get('nome') != None else '',
        				'parentesco': segurancaPessoa03['parentesco'] if segurancaPessoa03.get('parentesco') != None else ''
        			}
        		],
        		'autorizaoSaidaSozinho': event['seguranca']['autorizaoSaidaSozinho'] if event['seguranca'].get('autorizaoSaidaSozinho') != None else False,
        	},
        	'integral': {
        		'opcao': event['integral']['opcao'] if event['integral'].get('opcao') != None else False,
        		'qtdeDias': event['integral']['qtdeDias'] if event['integral'].get('qtdeDias') != None else 0,
        	}

        }
        
        response = table.put_item(
            TableName='EscolaSonhos_Matriculas',
            Item=params
        )
        print(response)
        
        # Atualiza o cadastro de AlunosMatr
        
        tableAlunosMatr = client.Table("EscolaSonhos_AlunosMatr")
        response = tableAlunosMatr.update_item(
            Key={
                'id': event['id']
            },
            UpdateExpression="set foiMatriculado = :p_foiMatriculado",
            ExpressionAttributeValues={
                ':p_foiMatriculado': True
            },
            ReturnValues="UPDATED_NEW"
        )
        print(response)
        
        return {
            'statusCode': 200,
            'headers': {},
            'body': json.dumps({'msg': 'Matricula realizada com sucesso!', 'id': params['id']})
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
