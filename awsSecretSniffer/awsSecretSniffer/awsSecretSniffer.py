import boto3
import re 

#setUp Session For AWS
awsUser = input("What is your AWS Key ID:")
awsSecret = input("What is your AWS Secret:")

# moved this to outside of the s3 bucket func
# that way the session object can be passed as a paramater if used in other functions
session = boto3.Session(
    aws_access_key_id=awsUser,
    aws_secret_access_key=awsSecret)

#Keyword, regex, entropy detection banks, etc

# Will update this with some fancier regex magic
keywordBank = ("password|passwd|pass|secret|api|token|key|cred|credentials")


#me trying to be fancy before I've had a chance to be basic. 
#regExBank = [
#    ("keyword", "keyword assignment", re.compile(r"(?i)[\w.\-]*(?:" + keywordBank + r")[\w.\-]*"
#        r"""\s*[:=]{1,2}>?\s*['"]?([^\s'"]{3,120})['"]?"""
#    ))
#    ]

#s3 Bucket Fucn
#Will refactor all this into an actual function
#Will have three modes
#Kitchen Sink == Searches ALL Buckets, ALL Files, for all secrets
#Paranoid, list bucket names and focuses on specific buckets and files to search for AWS secrets
#Recon collects bucket names, names of files in each bucket, exports it to a text file//html report to review later. But no string searches.

s3Client = session.client('s3')

response = s3Client.list_buckets()

bucketCount = 0



# Might split this into a count and then ask if they want to print all bucket names
for bucket in response['Buckets']:
    bucketCount = bucketCount + 1

print()
print("Total Buckets Found: " + str(bucketCount))
print()

listBucketsResponse = input("Would you like to list the Buckets now? (y/n)")
listBucketsResponse.lower()


if listBucketsResponse == "y" or "yes":
    print("These are the following buckets I can see:")
    print()
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

print()
print("Total Objects Found in " + targetBucket + ": " + str(objectCount))


#Ask For File
targetFile = input("Which file would you like to target?")

# Pull the File
response = s3Client.get_object(Bucket=targetBucket, Key=targetFile)

# Read and decode the text content
file_content = response['Body'].read().decode('utf-8')

#poor mans debugger
print(file_content)

# search the files

#test RegEx 
if re.search(keywordBank, file_content):
    print()
    print("Found a Hit")
    findAllMatches = re.findall(keywordBank,file_content,re.IGNORECASE)
    for foundMatch in findAllMatches:
        #currently this only prints the hit for the keyword not the value or chars surrounding it
        # will implement an inter to scrape the values around the match for better visability 
        print(foundMatch)

#s3 Glacier (Not sure how viable this will be)

#lambda Func
#lamdaObj = boto3.client('lambda')

#EFS Func

#FSx Func

#EBS Func

#MetaData Search Func?
