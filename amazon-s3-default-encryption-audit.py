# Import modules.
import boto3
import sys
import os
import time
import csv
from contextlib import suppress

# Print instructions for using the script.
print("")
print("Enter the output location for the report. For example: ")
print("")
print("Linux/Mac:  /home/documents/output/")
print("Windows:  c:/users/jsmith/documents/output/")
print("")
# Prompt user to input the output location of the report.
bucketEncryptionReportLocation = input("Output Location:  ")
bucketEncryptionReport = bucketEncryptionReportLocation + "bucketEncryptionReport_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"



# Define all the available AWS Regions (including opt-in regions).
regions_str = "us-east-1,us-east-2,us-west-1,us-west-2,af-south-1,ap-east-1,ap-south-1,ap-south-2,ap-northeast-1,ap-northeast-2,ap-northeast-3,ap-southeast-1,ap-southeast-2,ca-central-1,eu-central-1,eu-central-2,eu-west-1,eu-west-2,eu-west-3,eu-south-1,eu-south-2,eu-north-1,me-south-1,me-central-1,sa-east-1"
regions = regions_str.split(",")

# Create empty output files to store report.
open(bucketEncryptionReport, "a").close()


# Create function to add headers into the the CSV file.
def appendHeaders():
    #Specifying the headers to be added to the CSV file
    headers = ["Bucket Name", "Default Encryption Mode", "SSE-KMS Key Type", "Bucket Key"]
    #Opening the CSV file in write mode
    with open(bucketEncryptionReport, "w", newline="") as csvfile:
        #Creating a CSV writer object
        csvwriter = csv.writer(csvfile)
        #Writing the headers to the CSV file
        csvwriter.writerow(headers)

# Create function to print the data into the CSV file.
def report_info(file_name, details):
    # Print data into the CSV file.
    print(details, file=open(file_name, "a"),)



# Retrieve the default bucket encryption configuration for all buckets in all AWS Regions.
# Retrieve the default bucket encryption configuration for all buckets in all AWS Regions.
def sse_kms_bucket_logger():
    # Initialize the Amazon S3 boto3 client.
    s3 = boto3.client("s3")
    # Set the AWS_Default_Region environment variable to us-east-1 for this session.
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    # List all Amazon S3 buckets in the account.
    response = s3.list_buckets()
    # Retrieve the bucket name from the response
    buckets = response.get("Buckets")
    # Create a for loop to perform an action on all Amazon S3 buckets in the account.
    report_dict = []
    for bucket in buckets:
        with suppress(Exception):
            myBuckets = bucket.get("Name")
            # Sets s3 client region depending on the bucket
            response = s3.get_bucket_location(Bucket=myBuckets)
            location = response["LocationConstraint"]

            s3 = boto3.client("s3", region_name=location)
            endpointUrl = s3.meta.endpoint_url
            s3 = boto3.client("s3", endpoint_url=endpointUrl, region_name=location)
            try:
                # Run the GetBucketEncryption on all Amazon S3 buckets in all AWS Regions.
                # Determine the type of encryption key that is configured an Amazon S3 bucket and if Amazon S3 Bucket Key is enabled.
                resp = s3.get_bucket_encryption(Bucket=myBuckets)
                encryption_rules = resp.get("ServerSideEncryptionConfiguration", {}).get("Rules", [])
                if encryption_rules:
                    encryption = encryption_rules[0].get("ApplyServerSideEncryptionByDefault", {})
                    if "KMSMasterKeyID" in encryption:
                        kms_key = encryption["KMSMasterKeyID"]
                        bucketKey = str(encryption.get("BucketKeyEnabled", False))
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
                    else:
                        # Handle SSE-S3 encryption
                        sse_type = encryption.get("SSEAlgorithm", "SSE-S3")
                        report_info(
                            bucketEncryptionReport,
                            "{0}, {1}, {2}".format(myBuckets, sse_type, "N/A"),
                        )
                else:
                    # Handle case where no encryption configuration is found
                    report_info(
                        bucketEncryptionReport,
                        "{0}, {1}, {2}".format(myBuckets, "SSEConfigNotFound", "N/A"),
                    )

            except s3.exceptions.ClientError as e:
                error_code = e.response.get('Error', {}).get('Code')
                if error_code == 'AccessDenied':
                    # Catch and write AccessDenied errors when making the GetBucketEncryption API call.
                    # Check your AWS IAM policy and the Amazon S3 bucket policy to see if you have the s3:GetEncryptionConfiguration permissions for the Amazon S3 bucket.
                    report_info(
                        bucketEncryptionReport,
                        "{0}, {1}, {2}, {3}".format(myBuckets, "AccessDenied", "Unknown", "AccessDenied"),
                    )
                else:
                    raise
    return report_dict



# Determine if the SSE-KMS key being used is an AWS managed key or a customer managed key.
def key_type_check(reported_data, kms, region):
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
            except kms.exceptions.ClientError as e:
                error_code = e.response.get('Error', {}).get('Code')
                if error_code == "AccessDeniedException":
                    report_info(
                        bucketEncryptionReport,
                        "{0}, {1}, {2}, {3}".format(bucket, KMS_Key, "AccessDenied", bucketKeyStatus),
                    )
                elif error_code == "NotFoundException":
                    report_info(
                        bucketEncryptionReport,
                        "{0}, {1}, {2}, {3}".format(bucket, KMS_Key, "KeyNotFound", bucketKeyStatus),
                    )
                else:
                    raise





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
    appendHeaders()
    report_executor()


# Print the report's output location.
print("")
print("You can now access the report in the following location:  ")
print(bucketEncryptionReport)
