### Auditing Amazon S3 Default Encryption Configurations at Scale

## Overview of solution
In this post, I will describe how to audit an Amazon S3 bucket’s default encryption configuration at scale with a [Boto3](https://boto3.readthedocs.io/) script. I will show you how to configure the provided script to retrieve the default encryption configuration, KMS key ARN, KMS key type (AWS managed key or customer managed key), and the Amazon S3 Bucket Key configuration on all buckets in all regions. Finally, I will show you how to analyze the output to correlate the SSE configurations for each bucket. This script will perform the [ListBuckets](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListBuckets.html), [GetBucketLocation](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketLocation.html), [GetBucketEncryption](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketEncryption.html) API calls to all buckets in all regions. The script will then issue a DescribeKey API call to the AWS KMS key. 

The following services are used to audit the default server-side encryption mode:

  •	[Amazon S3](https://aws.amazon.com/s3/?nc=sn&loc=1)
  •	[AWS KMS](https://aws.amazon.com/kms/)

This script will perform read-only calls. No changes will be made to your resources.

## Prerequisites
You should have the following prerequisites: 

  •	An AWS account.
  •	Amazon S3 bucket.
  •	Python3 installed on your local machine. 
  •	AWS credentials to access your AWS account.
  •	Access to the **us-east-1** AWS Region.
  •	Permissions to perform the following actions:
    o	**s3:ListAllMyBuckets**
    o	**s3:GetBucketLocation**
    o	**s3:GetEncryptionConfiguration**
    o	**kms:DescribeKey**

The IAM policy for the IAM user or role that is running this script needs to have the following minimum Amazon S3 and AWS KMS permissions to retrieve the required information. 

The IAM policy for the IAM user or role that is running this script needs to have the following minimum Amazon S3 and AWS KMS permissions to retrieve the required information. 

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": " AllowS3ListingLocationAndEncryptionConfigRetrieval",
      "Action": [
        "s3:GetEncryptionConfiguration",
        “s3:GetBucketLocation”,
        "s3:ListAllMyBuckets"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::*"
    },
    {
      "Sid": "AllowAccesstoKmsKeyMetadata",
      "Action": [
        "kms:DescribeKey"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:kms:*:111111111111:key/*"
    }
  ]
```

You also need to ensure that the SSE-KMS customer managed keys allow the IAM role or user access as well. Click [here](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html#key-policy-default-allow-administrators) for more information about creating a KMS Key policy. 

## Walkthrough
# Download the script
Click [here](https://github.com/aws-samples/amazon-s3-default-encryption-audit) to download the script. 

# Execute the script
  1)	Open a terminal session on the device where the script is saved. 
  2)	Execute the script by running the following command:

```
$ python3 audit_s3_default_encryption.py

```
  3)	Input an output location for the report.
    
```
Linux/Mac:  /home/documents/output/
Windows:  c:/users/jsmith/documents/output/    
```
    
  4)	Wait for the script to complete. Depending on the amount of buckets and AWS KMS keys that you have configured, this can take several minutes. 
  5)	Navigate to the output location and open the report.

# Analyze the report
You will find the following example data:

| **Column A** | **Column B** | **Column C** | **Column D** |
| ---------| -------- | -------- | -------- |
| bucketA	| AES256	| N/A |                 | 
| bucketB	| SSEConfigNotFound	| N/A |       | 	
| bucketC	| AccessDenied	| Unknown	|       |
| bucketD	| arn:aws:kms:us-west-1:12345678908:key/111aa2bb-333c-4d44-…	| AccessDenied	| True |
| bucketE	| arn:aws:kms:us-east-1:12345678908:key/111aa2bb-333c-4d44-…	| CUSTOMER	| True     | 
| bucketF	| arn:aws:kms:ap-south-1:12345678908:key/666ww7xx-888y-9z99-…	| AWS 	|              | 
| bucketG	| arn:aws:kms:eu-east-2:98765432101:key/999ff5gg-000h-2i22-…	| Customer	| False    | 

The report is divided into four columns:

The report is divided into four columns:

  •	**Column A:** bucket name
  •	**Column B:** default bucket encryption mode
  •	**Column C:** customer managed key or an AWS managed key
  •	**Column D:** bucket key configuration
  
Column B can contain the following values:

  •	**AWS KMS Key ARN:** provides the ARN for the KMS Key that is configured in the bucket’s default encryption configuration. 
  •	**AWS KMS Key Alias:** provides the alias for the KMS Key that is configured in the bucket’s default encryption configuration. 
  •	**AES256:** indicates that the bucket is configured with SSE-S3 encryption. 
  •	**SSEConfigNotFound:** indicates that the bucket has no default encryption configurations.
  •	**AccessDenied:** indicates that the IAM user or role does not have the required permissions to perform the GetBucketEncryption API call.
  
Column C can the contain the following values:

  •	**CUSTOMER: indicates that the AWS KMS Key is an SSE-KMS customer managed key.
  •	**AWS:** indicates that the AWS KMS Key is an SSE-KMS AWS managed key. 
  •	**N/A:** indicates that SSE-KMS is not configured. 
  •	**AccessDenied:** indicates that the IAM user or role does not have the required permissions to perform the **DescribeKey** API call or that the AWS KMS key is located in a different AWS Region than the Amazon S3 bucket. 
  •	**Unknown:** indicates that the **DescribeKey** API call could not be performed because the **GetBucketEncryption** API call failed. 

Column D can the following values:

  •	**Null:** indicates that Bucket Key was never configured on this bucket. 
  •	**True:** indicates that Bucket Key is configured on this bucket. 
  •	**False:** indicates that Bucket Key was manually set to false.

This report can be used to standardize your default bucket encryption configurations across all buckets in all regions. You will be able to easily identify buckets that do not conform with your standardization requirements and identify buckets that do not have Amazon S3 Bucket Key enabled. Using the findings from this report, you will be able to create a plan to remediate buckets that do not follow your standardization requirements and buckets that are not taking advantage of Amazon S3 Bucket Key.

## Conclusion
In this post, I showed how you can audit your Amazon S3 bucket’s default encryption configuration at scale by using a Boto3 script. This can help you understand if you need to implement encryption standardizations or if encryption standardization practices are being followed. Using the generated output, you will be able to correlate all the different encryption types all buckets across all regions. Additionally, you will be able to understand which buckets are configured with Amazon S3 Bucket Key to ensure cost optimization features are enabled. Finally, you can also use this script to track which buckets have SSE-S3 enabled and which ones are still pending.


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

