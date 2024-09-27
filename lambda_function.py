import json
import boto3
import urllib.request
import urllib.parse
from botocore.exceptions import ClientError

USER_POOL_ID = "us-east-1_Ij0ntLjax"
CLIENT_ID = "2iq8rdjlfetjvabg0eekltes8"
SENHA='SENHA_PADRAO_123'

def calcular_digito(cpf, peso):
    soma = 0
    for i in range(peso):
        soma += int(cpf[i]) * (peso + 1 - i)
    digito = 11 - (soma % 11)
    return digito if digito < 10 else 0


def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    primeiro_digito = calcular_digito(cpf, 9)
    segundo_digito = calcular_digito(cpf, 10)
    return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"


def existe_usuario(cpf: str) -> bool:
    cognito = boto3.client('cognito-idp')
    try:
        cognito.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=cpf
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            return False
        raise e
        
def inserir_usuario(cpf: str, email: str, nome: str):
    cognito = boto3.client('cognito-idp')
    cognito.sign_up(
        ClientId=CLIENT_ID,
        Username=cpf,
        Password=SENHA,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            },
            {
                'Name': 'custom:cpf',
                'Value': cpf
            },
            {
                'Name': 'custom:nome',
                'Value': nome
            }
        ]
    )
    cognito.admin_confirm_sign_up(
        UserPoolId=USER_POOL_ID,
        Username=cpf
    )
    
def autenticar_usuario(cpf: str):
    cognito = boto3.client('cognito-idp')
    response = cognito.initiate_auth(
        ClientId=CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': cpf,
            'PASSWORD': SENHA
        }
    )
    return {
        "statusCode": 200,
        "body": json.dumps({
            "token": response['AuthenticationResult']['IdToken']
        })
    }
    

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        cpf = data['cpf']
        email = data['email']
        nome = data['nome']
        if not cpf or not email:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "CPF e email são obrigatórios."
                })
            }
        if not validar_cpf(cpf):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "CPF inválido."
                })
            }
            
        if not existe_usuario(cpf):
            inserir_usuario(cpf, email, nome)
        return autenticar_usuario(cpf)
    except ClientError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": str(e)
            })
        }
