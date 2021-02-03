import streamlit as st
import awswrangler as wr
import json
import pymysql
import pandas as pd
import datetime
import boto3
import uuid
import time



messagegroupID=uuid.uuid4()
messagedegroupID=uuid.uuid4()
sqs = boto3.client('sqs')
queue_url = "<ENTER SQS ARN>"
data = wr.secretsmanager.get_secret_json('<ENTER SECRETS ARN>')
conn =  pymysql.connect(host=data['host'],user=data['username'],password=data['password'],database='table1',port=data['port'])

def assignip():
    sql_query_1 = "select * from table1.table1  where status = 'available' order by RAND() limit 1"
    df = wr.mysql.read_sql_query(sql=sql_query_1,con=conn)
    dict_df = df.to_dict(orient='records')[0]
    sql_query_2 ="update table1 set status='not available' where id =" + str(int(df['id']))
    with conn.cursor() as cur:
        cur.execute(sql_query_2)
        conn.commit()
    dict_df['id']= str(dict_df['id'])
    del dict_df['Unnamed: 0']
    
    return dict_df

def send(n=1):
    for a in range(n):
        response = sqs.send_message(QueueUrl=queue_url,MessageBody=json.dumps(assignip()),MessageGroupId=str(messagegroupID))

def view():
    response = sqs.receive_message(QueueUrl=queue_url,MaxNumberOfMessages=1)
    return response

def delete(n=1):
    for a in range(n):
        response = view()
        response1 = json.loads(response['Messages'][0]['Body'])
        st.write("Your id for this ip is "+response1['id']+" And, the ip assigned to you is "+response1['ip_address'])
    try:
        response = sqs.delete_message(QueueUrl=queue_url,ReceiptHandle=response['Messages'][0]['ReceiptHandle'])
    except:
        print("No messages")


def purge():
    try: 
        response = sqs.purge_queue(QueueUrl=queue_url)
        st.info("Purging all the messages from the queue")
        time.sleep(60)
        st.success("Successfully Purged the Queue")
        
    except:
        print("Nothing to purge")

def releaseip(id):
    sql_query_2 ="update table1 set status='available' where id =" + str(id)
    st.write("Ip "+ str(id) +" released")

    with conn.cursor() as cur:
        cur.execute(sql_query_2)
        conn.commit()
        print("DONEEEE")
    st.write("Released "+str(id))

def listip(status=True):
    if status == True:
        sql_query  = "SELECT * FROM table1.table1 where status = 'available' ;" 
        df = wr.mysql.read_sql_query(sql=sql_query,con=conn)
        df = df.drop(columns=['Unnamed: 0','region'])
        st.dataframe(df)
    else:
        sql_query  = "SELECT * FROM table1.table1 where status = 'not available'; "
        df = wr.mysql.read_sql_query(sql=sql_query,con=conn)
        df = df.drop(columns=['Unnamed: 0','region'])
        st.dataframe(df)


st.title("Welcome to IPAM System")


radio_response = st.sidebar.radio("Select one of the following option", ['Get a new ip','List Currently Available IP','List Unavailable IPs'])
#submit = st.sidebar.button("Submit")
#purge = st.sidebar.button("Purge")


if radio_response == 'Get a new ip':
    send()
    delete()
if radio_response == 'Release an existing IP':
    num = st.text_input('Enter some text')
    if num:
        releaseip(int(num))
if radio_response == 'List Currently Available IP':
    listip(status=True)
if radio_response == 'List Unavailable IPs':
    listip(status=False)


        


