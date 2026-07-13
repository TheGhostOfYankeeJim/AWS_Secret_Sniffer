import boto3

#setUp Session For AWS
awsUser = input("What is your AWS Key ID:")
awsSecret = input("What is your AWS Secret:")



#s3 Bucket Fucn
#Will refactor all this into an actual function
#Will have three modes
#Kitchen Sink == Searches ALL Buckets, ALL Files, for all secrets
#Paranoid, list bucket names and focuses on specific buckets and files to search for AWS secrets
#Recon collects bucket names, names of files in each bucket, exports it to a text file//html report to review later. But no string searches.
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

print()
print("Total Buckets Found: " + str(bucketCount))

print()

listBucketsResponse = input("Would you like to list the Buckets now? (y/n)")
listBucketsResponse.lower()


if listBucketsResponse == "y" or "yes":
    for bucket in response['Buckets']:
        # poor mans debugger
        print(bucket['Name'])

#maybe a search bucket for sensitive strings func?
#CODE

# take bucket name func
targetBucket = input("Which bucket would you like to target?")
objectCount = 0

# Create paginator Obj for to hold the list of objects
paginator = s3Client.get_paginator('list_objects_v2')

# Create iterator for use in loop
page_iterator = paginator.paginate(Bucket=targetBucket)

# Loop
for page in page_iterator:
    if 'Contents' in page:
        for obj in page['Contents']:
            objectCount = objectCount + 1

            # poor mans debugger
            print(obj['Key'])





#s3 Glacier (Not sure how viable this will be)

#lambda Func
#lamdaObj = boto3.client('lambda')

#EFS Func

#FSx Func

#EBS Func

#MetaData Search Func?
