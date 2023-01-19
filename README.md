## Amazon S3 Default Encryption Audit

- This script will allow you to audit your Amazon S3 bucket's default encryption configuration for all buckets in all regions.
- You will need to modify line 10 in the script with the location that you want the output to be saved. 
- This script will NOT make any changes to AWS resources. 
- The "GetBucketEncryption" and the "DescribeKey" API call are used.
- You must have proper permissions to perform these API calls or else you will receive an AccessDenied error in the report. 
- If your Amazon S3 bucket is using SSE-KMS customer managed key that is NOT owned by the bucket owner's account, you will receive an AccessDenied error in the report. 


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

