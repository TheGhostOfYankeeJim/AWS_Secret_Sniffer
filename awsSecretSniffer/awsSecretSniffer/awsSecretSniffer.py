import boto3

#setUp Session For AWS
awsUser = input("What is your AWS Key ID:")
awsSecret = input("What is your AWS Secret:")



#s3 Bucket Fucn
session = boto3.Session(
    aws_access_key_id=awsUser,
    aws_secret_access_key=awsSecret)

s3Client = session.client('s3')

response = s3Client.list_buckets()

print("These are the following buckets I can see:")
for bucket in response['Buckets']:
    print(bucket['Name'])



#s3 Glacier (Not sure how viable this will be)

#lambda Func
lamdaObj = boto3.client('lambda')

#EFS Func

#FSx Func

#EBS Func
