import boto3
from datetime import datetime, timezone, timedelta
import csv  # Import necessário para trabalhar com arquivos CSV

Account_name = 'sandbox'
session = boto3.Session(profile_name=Account_name)
iam_client = session.client('iam')
days_old = 90
unused_roles = []



def list_unused_roles(event, context):
    try:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
        for page in iam_client.get_paginator('list_roles').paginate():
            for role in page['Roles']:
                role_name = role['RoleName']
                print(f'Verificando role :{role_name}')
                #obtem a ultima data de uso da role
                last_used_date = iam_client.get_role(RoleName=role_name)['Role'].get('RoleLastUsed',{}).get('LastUsedDate')
                
                if not last_used_date:
                    #role nunca foi usada
                    print(f"Role '{role_name}' nunca foi usada.\n")
                    unused_roles.append({'RoleName': role_name, 'LastUsedDate': 'Nunca usada'})
                elif last_used_date < cutoff_date:
                    #role está inativa há mais de X dias
                    print(f"Role '{role_name}' não utilizada desde: {last_used_date}\n")
                    unused_roles.append({'RoleName': role_name, 'LastUsedDate': last_used_date})
                    
                        
    except Exception as e:
        print(f"Erro ao listar roles: {e}")
    
    print(unused_roles)           
if __name__ == '__main__': list_unused_roles({},{})