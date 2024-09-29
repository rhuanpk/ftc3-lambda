# AWS Lambda com Integração ao Cognito

Este projeto fornece um endpoint de API serverless utilizando AWS Lambda, que verifica as credenciais do usuário (CPF, nome e email) e integra-se com o AWS Cognito para autenticação de usuários.

## Como funciona

1. **Payload**: O endpoint recebe um payload JSON com os seguintes campos:
    ```json
    {
      "cpf": "123.456.789-00",
      "nome": "João da Silva",
      "email": "joaodasilva@exemplo.com"
    }
    ```

2. **Validação de CPF**:
   - A função Lambda verifica se o `cpf` existe na base de dados.
   - Se o CPF existir, o usuário é autenticado e o token de acesso e retornado.
   - Se o CPF não existir, o usuário é registrado na base de dados com `cpf`, `nome` e `email` fornecidos e o token de acesso é gerado e retornado.
   
3. **AWS Cognito**:
   - É um serviço da AWS que permite gerenciar usuários.

## Como utilizar

URL: `https://jw1v21uqkj.execute-api.us-east-1.amazonaws.com/v1/autenticar-python`.

1. **Requisição**: Faça uma chamada POST com o payload JSON para a URL acima:
    ```json
    {
      "cpf": "123.456.789-00",
      "nome": "João da Silva",
      "email": "joaodasilva@exemplo.com"
    }
    ```
2. **Resposta 200**: Você receberá um Bearer token para de autenticação:
    ```json
    {
      "token": "eyJraWQiOiJLT1VRT2FFeUdQaT..."
    }
    ```
3. **Resposta 400**: Se o payload não for fornecido corretamente, você receberá uma resposta de erro:
    ```json
    {
      "message": "*****"
    }
    ```