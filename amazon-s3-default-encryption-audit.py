# Import modules.
import sys
import boto3
from botocore.exceptions import ClientError
import os
import csv
from re import search

# Define the report output location
bucketEncryptionReport = 'C:/outputs/bucketEncryptionReport.csv'

# Delete report file if it already exist.
try:
    os.remove(bucketEncryptionReport)
except:
    pass


# Create function to handle client errors (4xx errors).
def is_client_error(code):
    e = sys.exc_info()[1]
    if isinstance(e, ClientError) and e.response["Error"]["Code"] == code:
        return ClientError
    return type("NeverEverRaisedException", (Exception,), {})

# Initialize S3 client.
s3 = boto3.client('s3')

# Initialize KMS client on a per region basis.
kms = boto3.client('kms')
kms_use2 = boto3.client('kms',region_name='us-east-2',endpoint_url=('https://kms.us-east-2.amazonaws.com'))
kms_usw1 = boto3.client('kms',region_name='us-west-1',endpoint_url=('https://kms.us-west-1.amazonaws.com'))
kms_usw2 = boto3.client('kms',region_name='us-west-2',endpoint_url=('https://kms.us-west-2.amazonaws.com'))
kms_afs1 = boto3.client('kms',region_name='af-south-1',endpoint_url=('https://kms.af-south-1.amazonaws.com'))
kms_ape1 = boto3.client('kms',region_name='ap-east-1',endpoint_url=('https://kms.ap-east-1.amazonaws.com'))
kms_aps1 = boto3.client('kms',region_name='ap-south-1',endpoint_url=('https://kms.ap-south-1.amazonaws.com'))
kms_apne1 = boto3.client('kms',region_name='ap-northeast-1',endpoint_url=('https://kms.ap-northeast-1.amazonaws.com'))
kms_apne2 = boto3.client('kms',region_name='ap-northeast-2',endpoint_url=('https://kms.ap-northeast-2.amazonaws.com'))
kms_apne3 = boto3.client('kms',region_name='ap-northeast-3',endpoint_url=('https://kms.ap-northeast-3.amazonaws.com'))
kms_apse1 = boto3.client('kms',region_name='ap-southeast-1',endpoint_url=('https://kms.ap-southeast-1.amazonaws.com'))
kms_apse2 = boto3.client('kms',region_name='ap-southeast-2',endpoint_url=('https://kms.ap-southeast-2.amazonaws.com'))
kms_cac1 = boto3.client('kms',region_name='ca-central-1',endpoint_url=('https://kms.ca-central-1.amazonaws.com'))
kms_cnn1 = boto3.client('kms',region_name='cn-north-1',endpoint_url=('https://kms.cn-north-1.amazonaws.com'))
kms_cnnw1 = boto3.client('kms',region_name='cn-northwest-1',endpoint_url=('https://kms.cn-northwest-1.amazonaws.com'))
kms_euc1 = boto3.client('kms',region_name='eu-central-1',endpoint_url=('https://kms.eu-central-1.amazonaws.com'))
kms_euw1 = boto3.client('kms',region_name='eu-west-1',endpoint_url=('https://kms.eu-west-1.amazonaws.com'))
kms_euw2 = boto3.client('kms',region_name='eu-west-2',endpoint_url=('https://kms.eu-west-2.amazonaws.com'))
kms_euw3 = boto3.client('kms',region_name='eu-west-3',endpoint_url=('https://kms.eu-west-3.amazonaws.com'))
kms_eus1 = boto3.client('kms',region_name='eu-south-1',endpoint_url=('https://kms.eu-south-1.amazonaws.com'))
kms_eun1 = boto3.client('kms',region_name='eu-north-1',endpoint_url=('https://kms.eu-north-1.amazonaws.com'))
kms_mes1 = boto3.client('kms',region_name='me-south-1',endpoint_url=('https://kms.me-south-1.amazonaws.com'))
kms_sae1 = boto3.client('kms',region_name='sa-east-1',endpoint_url=('https://kms.sa-east-1.amazonaws.com'))


# Create temporary CSV files. The script will remove all these files once it finishes running..
KMS_Output = 'KMS_Buckets.csv'
Full_NotFound_Report = 'Full_NotFound_Report.csv'

key_ids_use1 = 'KEY_IDS_us-east-1.csv'
key_ids_use2 = 'KEY_IDS_us-east-2.csv'
key_ids_usw1 = 'KEY_IDS_us-west-1.csv'
key_ids_usw2 = 'KEY_IDS_us-west-2.csv'
key_ids_afs1 = 'KEY_IDS_af-south-1.csv'
key_ids_ape1 = 'KEY_IDS_ap-east-1.csv'
key_ids_aps1 = 'KEY_IDS_ap-south-1.csv'
key_ids_apne1 = 'KEY_IDS_ap-northeast-1.csv'
key_ids_apne2 = 'KEY_IDS_ap-northeast-2.csv'
key_ids_apne3 = 'KEY_IDS_ap-northeast-3.csv'
key_ids_apse1 = 'KEY_IDS_ap-southeast-1.csv'
key_ids_apse2 = 'KEY_IDS_ap-southeast-2.csv'
key_ids_cac1 = 'KEY_IDS_ca-central-1.csv'
key_ids_cnn1 = 'KEY_IDS_cn-north-1.csv'
key_ids_cnnw1 = 'KEY_IDS_cn-northwest-1.csv'
key_ids_euc1 = 'KEY_IDS_eu-central-1.csv'
key_ids_euw1 = 'KEY_IDS_eu-west-1.csv'
key_ids_euw2 = 'KEY_IDS_eu-west-2.csv'
key_ids_euw3 = 'KEY_IDS_eu-west-3.csv'
key_ids_eus1 = 'KEY_IDS_eu-south-1.csv'
key_ids_eun1 = 'KEY_IDS_eu-north-1.csv'
key_ids_mes1 = 'KEY_IDS_me-south-1.csv'
key_ids_sae1 = 'KEY_IDS_sa-east-1.csv'








# Create empty output files so that the code can append each bucket to the respective files.
open(KMS_Output, 'a').close()
open(Full_NotFound_Report, 'a').close()

open(key_ids_use1, 'a').close()
open(key_ids_use2, 'a').close()
open(key_ids_usw1, 'a').close()
open(key_ids_usw2, 'a').close()
open(key_ids_afs1, 'a').close()
open(key_ids_ape1, 'a').close()
open(key_ids_aps1, 'a').close()
open(key_ids_apne1, 'a').close()
open(key_ids_apne2, 'a').close()
open(key_ids_apne3, 'a').close()
open(key_ids_apse1, 'a').close()
open(key_ids_apse2, 'a').close()
open(key_ids_cac1, 'a').close()
open(key_ids_cnn1, 'a').close()
open(key_ids_cnnw1, 'a').close()
open(key_ids_euc1, 'a').close()
open(key_ids_euw1, 'a').close()
open(key_ids_euw2, 'a').close()
open(key_ids_euw3, 'a').close()
open(key_ids_eus1, 'a').close()
open(key_ids_eun1, 'a').close()
open(key_ids_mes1, 'a').close()
open(key_ids_sae1, 'a').close()

open(bucketEncryptionReport, 'a').close()



# Create variables for regional KMS Key ARNs:
key_region_use1 = 'arn:aws:kms:us-east-1'
key_region_use2 = 'arn:aws:kms:us-east-2'
key_region_usw1 = 'arn:aws:kms:us-west-1'
key_region_usw2 = 'arn:aws:kms:us-west-2'
key_region_afs1 = 'arn:aws:kms:af-south-1'
key_region_ape1 = 'arn:aws:kms:ap-east-1'
key_region_aps1 = 'arn:aws:kms:ap-south-1'
key_region_apne1 = 'arn:aws:kms:ap-northeast-1'
key_region_apne2 = 'arn:aws:kms:ap-northeast-2'
key_region_apne3 = 'arn:aws:kms:ap-northeast-3'
key_region_apse1 = 'arn:aws:kms:ap-southeast-1'
key_region_apse2 = 'arn:aws:kms:ap-southeast-2'
key_region_cac1 = 'arn:aws:kms:ca-central-1'
key_region_cnn1 = 'arn:aws:kms:cn-north-1'
key_region_cnnw1 = 'arn:aws:kms:cn-northwest-1'
key_region_euc1 = 'arn:aws:kms:eu-central-1'
key_region_euw1 = 'arn:aws:kms:eu-west-1'
key_region_euw2 = 'arn:aws:kms:eu-west-2'
key_region_euw3 = 'arn:aws:kms:eu-west-3'
key_region_eus1 = 'arn:aws:kms:eu-south-1'
key_region_eun1 = 'arn:aws:kms:eu-north-1'
key_region_mes1 = 'arn:aws:kms:me-south-1'
key_region_sae1 = 'arn:aws:kms:sa-east-1'




# List all buckets in the account.
response = s3.list_buckets()

# Get the bucket name from the response
buckets = response.get('Buckets')

# Create a for loop to peform an action on all the buckets in the account.
for bucket in buckets:
    myBuckets = bucket.get('Name')

    # Print buckets that are configured with SSE-KMS (AWS Managed & Customer Managed) encryption keys.
    try:
        resp = s3.get_bucket_encryption(Bucket=myBuckets)
        kms_key = resp['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['KMSMasterKeyID']
        bucketKey = resp['ServerSideEncryptionConfiguration']['Rules'][0]['BucketKeyEnabled']
        print(myBuckets+', '+kms_key, file=open(KMS_Output, "a"))
        if kms_key.startswith(key_region_use1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_use1, "a"))
        if kms_key.startswith(key_region_use2):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_use2, "a"))
        if kms_key.startswith(key_region_usw1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_usw1, "a"))
        if kms_key.startswith(key_region_usw2):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_usw2, "a"))
        if kms_key.startswith(key_region_afs1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_afs1, "a"))
        if kms_key.startswith(key_region_ape1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_ape1, "a"))
        if kms_key.startswith(key_region_aps1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_aps1, "a"))
        if kms_key.startswith(key_region_apne1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_apne1, "a"))
        if kms_key.startswith(key_region_apne2):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_apne2, "a"))
        if kms_key.startswith(key_region_apne3):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_apne3, "a"))
        if kms_key.startswith(key_region_apse1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_apse1, "a"))
        if kms_key.startswith(key_region_apse2):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_apse2, "a"))
        if kms_key.startswith(key_region_cac1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_cac1, "a"))
        if kms_key.startswith(key_region_cnn1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_cnn1, "a"))
        if kms_key.startswith(key_region_cnnw1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_cnnw1, "a"))
        if kms_key.startswith(key_region_euc1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_euc1, "a"))
        if kms_key.startswith(key_region_euw1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_euw1, "a"))
        if kms_key.startswith(key_region_euw2):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_euw2, "a"))
        if kms_key.startswith(key_region_euw3):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_euw3, "a"))
        if kms_key.startswith(key_region_eus1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_eus1, "a"))
        if kms_key.startswith(key_region_eun1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_eun1, "a"))
        if kms_key.startswith(key_region_mes1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_mes1, "a"))
        if kms_key.startswith(key_region_sae1):
        	print(myBuckets+', '+kms_key+', '+bucketKey, file=open(key_ids_sae1, "a"))




    # Print buckets that are configured with SSE-S3 (AES256) encryption keys.
    except KeyError as b:
        sse_type = resp['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
        print(myBuckets+', '+sse_type+', N/A', file=open(bucketEncryptionReport, "a"))


    # Print buckets that are threw a HTTP 403 AccessDenied error when making the GetBucketEncryption API call.
    except is_client_error('AccessDenied'):
        print(myBuckets+', AccessDenied, N/A', file=open(bucketEncryptionReport, "a"))

    # Print buckets where no Default Encryption Configurations were found.
    except is_client_error('ServerSideEncryptionConfigurationNotFoundError'):
        print(myBuckets+', SSEConfigNotFound, N/A', file=open(bucketEncryptionReport, "a"))











###################################################################################################################
#### These Functions will check to see if the KMS Key is an AWS Managed KMS Key or a Customer Managed KMS Key. ####
###################################################################################################################



def useast1():
    filename = key_ids_use1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def useast2():
    filename = key_ids_use2
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_use2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def uswest1():
    filename = key_ids_usw1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def uswest2():
    filename = key_ids_usw2
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def afsouth1():
    filename = key_ids_afs1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def apeast1():
    filename = key_ids_ape1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def apsouth1():
    filename = key_ids_aps1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def apnortheast1():
    filename = key_ids_apne1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def apnortheast2():
    filename = key_ids_apne2
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def apnortheast3():
    filename = key_ids_apne3
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def apsoutheast1():
    filename = key_ids_apse1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))


def apsoutheast2():
    filename = key_ids_apse2
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def cacentral1():
    filename = key_ids_cac1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def cnnorth1():
    filename = key_ids_cnn1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def cnnorthwest1():
    filename = key_ids_cnnw1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def eucentral1():
    filename = key_ids_euc1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def euwest1():
    filename = key_ids_euw1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def euwest2():
    filename = key_ids_euw2
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def euwest3():
    filename = key_ids_euw3
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def eusouth1():
    filename = key_ids_eus1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def eunorth1():
    filename = key_ids_eun1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def mesouth1():
    filename = key_ids_mes1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))

def saeast1():
    filename = key_ids_sae1
    # Initializing the rows list.
    rows = []
    # Reading csv file.
    with open(filename, 'r') as csvfile:
        # Creating a csv reader object.
        csvreader = csv.reader(csvfile)
        # Extracting each data row one by one.
        for row in csvreader:
            # Provide a title for each row.
            bucket = row[0]
            KMS_Key_modify = row[1]
            bucketKeyStatus = row[2]
            KMS_Key = KMS_Key_modify[1:]
            try:
                response = kms_usw2.describe_key(KeyId=KMS_Key)
                key_type = response['KeyMetadata']['KeyManager']
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+key_type+', '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))
            except is_client_error('NotFoundException'):
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus)
                print(bucket+', '+KMS_Key+', '+bucketKeyStatus, file=open(Full_NotFound_Report, "a"))
                print(bucket+', '+KMS_Key+', N/A, '+bucketKeyStatus, file=open(bucketEncryptionReport, "a"))



if __name__ == '__main__' :
    useast1()
    useast2()
    uswest1()
    uswest2()
    afsouth1()
    apeast1()
    apsouth1()
    apnortheast3()
    apnortheast2()
    apnortheast1()
    apsoutheast1()
    apsoutheast2()
    cacentral1()
    cnnorth1()
    cnnorthwest1()
    eucentral1()
    euwest3()
    euwest2()
    euwest1()
    eusouth1()
    eunorth1()
    mesouth1()
    saeast1()






os.remove(key_ids_use1)
os.remove(key_ids_use2)
os.remove(key_ids_usw1)
os.remove(key_ids_usw2)
os.remove(key_ids_afs1)
os.remove(key_ids_ape1)
os.remove(key_ids_aps1)
os.remove(key_ids_apne1)
os.remove(key_ids_apne2)
os.remove(key_ids_apne3)
os.remove(key_ids_apse1)
os.remove(key_ids_apse2)
os.remove(key_ids_cac1)
os.remove(key_ids_cnn1)
os.remove(key_ids_cnnw1)
os.remove(key_ids_euc1)
os.remove(key_ids_euw1)
os.remove(key_ids_euw2)
os.remove(key_ids_euw3)
os.remove(key_ids_eus1)
os.remove(key_ids_eun1)
os.remove(key_ids_mes1)
os.remove(key_ids_sae1)
