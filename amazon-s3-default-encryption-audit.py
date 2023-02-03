# Import modules.
import sys
import boto3
from botocore.exceptions import ClientError
import time
import os
import csv
import json
from re import search



# Print instructions for using the script.
print('')
print('Enter the output location for the report. For example: ')
print('')
print('Linux/Mac:  /home/documents/output/')
print('Windows:  c:/users/jsmith/documents/output/')
print('')
# Prompt user to input the output location of the report.
bucketEncryptionReportLocation = input('Output Location:  ')
bucketEncryptionReport = bucketEncryptionReportLocation + 'bucketEncryptionReport_' + time.strftime("%Y%m%d-%H%M%S") + '.csv'



# Define all the available AWS Regions (including opt-in regions).
regions_str = 'us-east-1,us-east-2,us-west-1,us-west-2,af-south-1,ap-east-1,ap-south-1,ap-south-2,ap-northeast-1,ap-northeast-2,ap-northeast-3,ap-southeast-1,ap-southeast-2,ca-central-1,eu-central-1,eu-central-2,eu-west-1,eu-west-2,eu-west-3,eu-south-1,eu-south-2,eu-north-1,me-south-1,me-central-1,sa-east-1'
regions = regions_str.split(",")

# Create empty output files to store report.
open(bucketEncryptionReport, "a").close()

# Create function to handle client errors (4xx errors).
def is_client_error(code):
    e = sys.exc_info()[1]
    if isinstance(e, ClientError) and e.response["Error"]["Code"] == code:
        return ClientError
    return type("NeverEverRaisedException", (Exception,), {})

# Create function to print the data into the CSV file.
def report_info(file_name, details):
    print(
        details,
        file=open(file_name, "a"),
    )



# Retrieve the default bucket encryption configuration for all buckets in all AWS Regions.
def sse_kms_bucket_logger():
    # Initialize the Amazon S3 boto3 client.
    s3 = boto3.client("s3")
    # List all Amazon S3 buckets in the account.
    response = s3.list_buckets()
    # Retrieve the bucket name from the response
    buckets = response.get("Buckets")
    # Create a for loop to peform an action on all Amazon S3 buckets in the account.
    report_dict = []
    for bucket in buckets:
        myBuckets = bucket.get("Name")
        #sets s3 client region depending on the bucket
        response = s3.get_bucket_location(Bucket=myBuckets)
        location=response['LocationConstraint']
        s3 = boto3.client('s3', region_name=location)
        endpointUrl = s3.meta.endpoint_url
        s3 = boto3.client('s3', endpoint_url=endpointUrl, region_name=location)
        try:
            # Run the GetBucketEncryption on all Amazon S3 buckets in all AWS Regions.
            # Determine the type of encryption key that is configured an Amazon S3 bucket and if Amazon S3 Bucket Key is enabled.
            resp = s3.get_bucket_encryption(Bucket=myBuckets)
            kms_key = resp["ServerSideEncryptionConfiguration"]["Rules"][0][
                "ApplyServerSideEncryptionByDefault"
            ]["KMSMasterKeyID"]
            bucketKey = str(
                resp["ServerSideEncryptionConfiguration"]["Rules"][0][
                    "BucketKeyEnabled"
                ]
            )
            for region in regions:
                # Create variables for regional KMS Key ARNs:
                key_region_arn = "arn:aws:kms:{0}".format(region)
                if kms_key.startswith(key_region_arn):
                    data = {
                        "region": region,
                        "bucket": myBuckets,
                        "kmsKey": kms_key,
                        "bucketStatus": bucketKey,
                    }
                    report_dict.append(data)
        except KeyError as b:
            # Print buckets that are configured with SSE-S3 encryption keys.
            sse_type = resp["ServerSideEncryptionConfiguration"]["Rules"][0][
                "ApplyServerSideEncryptionByDefault"
            ]["SSEAlgorithm"]
            report_info(
                bucketEncryptionReport,
                "{0}, {1}, {2}".format(myBuckets, sse_type, "N/A"),
            )
        except is_client_error("ServerSideEncryptionConfigurationNotFoundError"):
            # Print buckets where no Default Encryption Configurations were found.
            report_info(
                bucketEncryptionReport,
                "{0}, {1}, {2}".format(myBuckets, "SSEConfigNotFound", "N/A"),
            )
        except is_client_error("AccessDenied"):
            # Catch and write AccessDenied errors when making the GetBucketEncryption API call.
            # Check your AWS IAM policy and the Amazon S3 bucket policy to see if you have the s3:GetEncryptionConfiguration permissions for the Amazon S3 bucket.
            report_info(
                bucketEncryptionReport,
                "{0}, {1}, {2}".format(myBuckets, "AccessDenied", "Unknown", "Unknown"),
            )
    return report_dict



# Determine if the SSE-KMS key being used is an AWS managed key or a customer managed key.
def key_type_check(reported_data, kms,region):
    for item in reported_data:
        # Provide a title for each row.
        if region == item["region"]:
            bucket = item["bucket"]
            KMS_Key = item["kmsKey"]
            bucketKeyStatus = item["bucketStatus"]
            try:
                # Run the DescribeKey API to determine if the AWS KMS Key is an AWS managed key or a customer managed key.
                response = kms.describe_key(KeyId=KMS_Key)
                key_type = response["KeyMetadata"]["KeyManager"]
                report_info(
                    bucketEncryptionReport,
                    "{0}, {1}, {2}, {3}".format(bucket, KMS_Key, key_type, bucketKeyStatus),
                )
            # Catch and write AccessDenied errors when performing the DescribeKey API.
            # Check your AWS IAM Policy and AWS KMS key permissions to see if you have the kms:DescribeKey permissions for the AWS KMS key.
            # Check to to see if the AWS KMS key is located in the same AWS Region as your Amazon S3 bucket.
            except is_client_error("AccessDeniedException"):
                report_info(
                    bucketEncryptionReport,
                    "{0}, {1}, {2}, {3}".format(
                        bucket, KMS_Key, "AccessDenied", bucketKeyStatus
                    ),
                )
            # Catch and write NotFoundException errors when performing the DescribeKey API.
            # CHeck to see if the AWS KMS key is valid.
            except is_client_error("NotFoundException"):
                report_info(
                    bucketEncryptionReport,
                    "{0}, {1}, {2}, {3}".format(
                        bucket, KMS_Key, "keyNotFound", bucketKeyStatus
                    ),
                )



# Define reporting function.
def report_executor():
    #Loop through all AWS Regions
    reported_data = sse_kms_bucket_logger()
    for region in regions:
        #Initialize KMS client on a per region basis.
        url = "https://kms.{0}.amazonaws.com".format(region)
        kms = boto3.client("kms", region_name=region, endpoint_url=(url))
        key_type_check(reported_data, kms,region)



# Execute report function.
if __name__ == '__main__' :
    report_executor()



# Print the report's output location.
print("")
print('You can now access the report in the following location:  ')
print(bucketEncryptionReport)
