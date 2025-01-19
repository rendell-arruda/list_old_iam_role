import boto3
from datetime import datetime, timezone, timedelta

#VARIABLES
#account name 
account_name = 'sandbox' 
#qtdd de dias para considerar uma role como inativa.
days_old = 90
#list de roles consideradas inativas
unused_roles = []

session = boto3.Session(profile_name=account_name)
iam_client = session.client('iam')

def lambda_handler(event, context):
    try:
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
        
        # list roles
        for page in iam_client.get_paginator('list_roles').paginate():
            for role in page['Roles']:
                role_name = role['RoleName']
                print(f"Verificando role: {role_name}")
                
                # get last used date
                role_info = iam_client.get_role(RoleName=role_name)
                last_used_date = role_info['Role'].get('RoleLastUsed',{}).get('LastUsedDate')

                
    except Exception as e:
        print(f"Erro ao listar roles: {e}")
 
if __name__ == '__main__': 
    lambda_handler({},{})