import boto3
from datetime import datetime, timezone
import csv

Account_name = 'sandbox'
session = boto3.Session(profile_name=Account_name)
iam_client = session.client('iam')
days_old = 90
unused_roles = []



def list_unused_roles(event, context):
    try:
        for page in iam_client.get_paginator('list_roles').paginate():
            for role in page['Roles']:
                role_name = role['RoleName']
                print(role_name)
    except Exception as e:
        print(f"Erro ao listar roles: {e}")
               
if __name__ == '__main__': list_unused_roles({},{})