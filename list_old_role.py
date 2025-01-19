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
        
        
    except Exception as e:
        print(f"Erro ao listar roles: {e}")
 
if __name__ == '__main__': 
    lambda_handler({},{})