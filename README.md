## Amazon S3 Default Encryption Audit

- This script will allow you to audit your [Amazon S3](https://aws.amazon.com/s3/) bucket's default encryption and the [Amazon S3 Bucket Key](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html) configuration for all buckets in all regions.
- The script is configured to list all your buckets in all regions, then retrieve teh 
- You will need to **modify line 10** in the script with the location that you want the output to be saved. 
- This script will NOT make any changes to AWS resources. 
- The [ListBuckets](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListBuckets.html), [GetBucketEncryption](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetBucketEncryption.html) and the [DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html) API call are used.
- You must have proper permissions to perform these API calls or else you will receive an AccessDenied error in the report. 
- If your Amazon S3 bucket is using SSE-KMS customer managed key that is NOT owned by the bucket owner's account, you will receive an AccessDenied error in the report. 


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

