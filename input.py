import awswrangler as wr
import json
import pymysql
import pandas as pd
import datetime
import boto3

### Import DB credentials from AWS Secrets Manager
data = wr.secretsmanager.get_secret_json('<ENTER ARN>')

conn =  pymysql.connect(host=data['host'],user=data['username'],password=data['password'],database='table1')

df = pd.read_csv('data.csv')
wr.mysql.to_sql(df=df,con=conn,table='table1',schema='table1',mode='overwrite') 