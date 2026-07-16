import boto3
import re 
import argparse

def setAuth():
    #setUp Session For AWS
    awsUser = input("What is your AWS Key ID:")
    awsSecret = input("What is your AWS Secret:")

    # moved this to outside of the s3 bucket func
    # that way the session object can be passed as a paramater if used in other functions
    session = boto3.Session(aws_access_key_id=awsUser,aws_secret_access_key=awsSecret)
    return session

def s3WatchListMode():
    # Will update this with some fancier regex magic
    keywordBank = ("password|passwd|pass|secret|api|token|key|cred|credentials")

    #fancy regexs I found online 
    patternsBank = {
    "AWS Access Key": r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b",
    "GitHub Token":   r"\bghp_[0-9A-Za-z]{36}\b",
    "Slack Token":    r"\bxox[baprs]-[0-9A-Za-z-]{10,72}\b",
    "Stripe Key":     r"\b(?:sk|rk)_(?:live|test)_[0-9a-zA-Z]{24,}\b",
    "API Key":        r"\bsk-(?:ant-)?[0-9A-Za-z-]{20,}\b",
    "JWT":            r"\beyJ[\w-]+\.[\w-]+\.[\w-]+\b",
    "Private Key":    r"-----BEGIN (?:\w+ )?PRIVATE KEY-----",
    }

    hashesBank = {
        "bcrypt hash":    r"\$2[abxy]\$\d{2}\$[./A-Za-z0-9]{53}",
        "hex hash":       r"\b[a-fA-F0-9]{32,128}\b",
     }


    sessionAWS = setAuth()
    s3Client = sessionAWS.client('s3')
    response = s3Client.list_buckets()
    bucketCount = 0

    print()
    print("*********************")
    print("Total Buckets Found: " + str(bucketCount))
    print("*********************")
    print()

    listBucketsResponse = input("Would you like to list the Buckets now? (y/n)")
    listBucketsResponse.lower()


    if listBucketsResponse == "y" or "yes":
        print("These are the following buckets I can see:")
        print()
        for bucket in response['Buckets']:
            # poor mans debugger
            print(bucket['Name'])

    #maybe a search bucket name for sensitive strings func?
    #CODE

    # take bucket name func
    print()
    targetBucket = input("Which bucket would you like to target?")
    objectCount = 0
    print()

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
    print("*********************")
    print("Total Objects Found in " + targetBucket + ": " + str(objectCount))
    print("*********************")
    print()

    #Ask For File
    targetFile = input("Which file would you like to target?")

    # Pull the File
    response = s3Client.get_object(Bucket=targetBucket, Key=targetFile)

    # Read and decode the text content
    file_content = response['Body'].read().decode('utf-8')

    #poor mans debugger
    print(file_content)

    print()
    print("*********************")
    print("Searching KEYWORDS:")
    print("*********************")
    print()

    # Search Function For KeywordBank
    for line in file_content.splitlines():
        if re.search(keywordBank,line,re.IGNORECASE):
            print(line)

    print()
    print("*********************")
    print("Searching PATTERNS:")
    print("*********************")
    print()

    for label, pattern in patternsBank.items():
        for matchPattern in re.finditer(pattern,file_content):
            print(label + ": " + matchPattern.group())


def main():
    # 1. Initialize the parser
    parser = argparse.ArgumentParser(
        description="AWS Secret Sniffer."
    )

    # 2. Add a required positional argument (order matters)
    parser.add_argument(
        "AWS_Service", 
        type=str, 
        help="S3 Only So Far"
    
    )
    parser.add_argument(
        "--watchlist", action="store_true", help="Enable watchlist mode."
        )
    args = parser.parse_args()
    
    if args.AWS_Service == "S3" and args.watchlist:
        print("Starting: " + args.AWS_Service + " in WatchList Mode")
        print("Starting S3 Watchlist Mode")
        s3WatchListMode()

# Main Function Loop
if __name__ == "__main__":
    main()

#s3 Bucket Fucn
#Will refactor all this into an actual function
#Will have three modes
#Kitchen Sink == Searches ALL Buckets, ALL Files, for secrets
#Paranoid, list bucket names and focuses on one specific bucket but search all the files for secrets
#WatchList, Specific Bucket and Specific File searches.
#maybe just a numerical data return, how many buckets, files, public vs private, buckets without access etc. 


#s3 Glacier (Not sure how viable this will be)

#lambda Func
#lamdaObj = boto3.client('lambda')

#EFS Func

#FSx Func

#EBS Func

#MetaData Search Func?