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

bucketCount = 0

print("These are the following buckets I can see:")

# Might split this into a count and then ask if they want to print all bucket names
for bucket in response['Buckets']:
    bucketCount = bucketCount + 1

    # poor mans debugger
    print(bucket['Name'])

print("Total Buckets Found: " + str(bucketCount))

# take bucket name func
# CODE

# list contents of buckets





#s3 Glacier (Not sure how viable this will be)

#lambda Func
#lamdaObj = boto3.client('lambda')

#EFS Func

#FSx Func

#EBS Func
