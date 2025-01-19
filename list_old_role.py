import boto3
from datetime import datetime, timezone, timedelta
import csv

#VARIABLES
#account name 
account_name = 'sandbox' 
#qtdd de dias para considerar uma role como inativa.
days_old = 60
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

                #verify if role was used
                if not last_used_date:
                    print(f'Role {role_name} nunca foi usada.\n')
                    unused_roles.append({'RoleName': role_name, 'LastUsedDate': 'Nunca usada'})
                else:
                    #verify if role is out of the allowed period
                    time_difference = datetime.now(timezone.utc) - last_used_date
                    #chech if the role is older than 90 days considering 86400 seconds in a day
                    if time_difference.total_seconds() > days_old * 86400:
                        print(f'Role {role_name} não utilizada desde: {last_used_date}\n')
                        unused_roles.append({'RoleName': role_name, 'LastUsedDate': last_used_date})    
                
        #export results to a csv file
        with open('unused_roles.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['RoleName', 'LastUsedDate'])
            writer.writeheader()
            writer.writerows(unused_roles)
        
        print(f"\n{len(unused_roles)} roles não utilizadas encontradas. Detalhes salvos em 'unused_roles.csv'.")
                
    except Exception as e:
        print(f"Erro ao listar roles: {e}")
     
if __name__ == '__main__': 
    lambda_handler({},{})