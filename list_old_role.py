import boto3
from datetime import datetime, timezone
import csv

Account_name = 'sandbox'
session = boto3.Session(profile_name=Account_name)
iam_client = session.client('iam')
days_old = 90
unused_roles = []



def list_unused_roles(event, context):
    
    response = iam_client.list_roles()
    print(response)
    for role in response['Roles']:
        role_name = role['RoleName']
        print(role_name)
 
if __name__ == '__main__': list_unused_roles({},{})