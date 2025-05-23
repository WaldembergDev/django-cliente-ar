from dotenv import load_dotenv
import os
import requests
from pprint import pprint

load_dotenv()

def obter_dados_cnpj(cnpj: str):

    result = requests.get(f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}')

    try:
        result.raise_for_status()
        dados = result.json()
        # razao social
        razao_social = dados.get('razao_social')
        # cep
        cep = dados.get('cep')
        # logradouro
        logradouro = dados.get('logradouro')
        # numero
        numero = dados.get('numero')
        # complemento
        complemento = dados.get('complemento')
        # bairro
        bairro = dados.get('bairro')
        # municipio
        municipio = dados.get('municipio')
        # telefone
        telefone = dados.get('ddd_telefone_1')
        # email
        email = dados.get('email')
        # dicionario resultados
        dados_resultado = {
            'razao_social': razao_social,
            'cep': cep,
            'logradouro': logradouro,
            'numero': numero,
            'complemento': complemento,
            'bairro': bairro,
            'municipio': municipio,
            'telefone': telefone,
            'email': email
        }
        return dados
    except Exception as e:
        print(f'Erro gerado: {e}')
        return None