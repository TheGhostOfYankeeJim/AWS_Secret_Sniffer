from tokenize import Ignore

import boto3
import re 
import argparse

###################################################################
# Global Vars
# Will update this with some fancier regex magic
###################################################################

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

########################## End Of Global Vals #################################


# Set up auth so the credentials do get saved in history or on disk
def setAuth():
    # Get Credential Info
    awsUser = input("What is your AWS Key ID: ")
    awsSecret = input("What is your AWS Secret: ")

   
    # creates session object with supplied creds, and returns the session object to be used elsewhere
    session = boto3.Session(aws_access_key_id=awsUser,aws_secret_access_key=awsSecret)
    return session

#############################
# S3 Sniffer Methods
#############################

def s3KitchenSinkMode():

    sessionAWS = setAuth()
    s3Client = sessionAWS.client('s3')
    response = s3Client.list_buckets()
    bucketCount = 0
    fileCount = 0

    



    for bucket in response['Buckets']:
        bucketCount += 1
        bucketTarget = bucket['Name']
        paginator = s3Client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucketTarget)
        
        # Loop
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    fileCount = fileCount + 1


    print()
    print("*********************")
    print("Total Buckets Found: " + str(bucketCount))
    print("*********************")
    print()



    print()
    print("*********************")
    print("Total Files Found: " + str(fileCount) )
    print("*********************")
    print()

    wantToContine = input("Would you like to search every file on every bucket?")

    # Might be worth to create either a JSON/List/whatever object, that holds all the things found
    # like Found possible keys in: 
    # Bucket <NAME>
    # List of Files 
    # Right now the way this functionality works its overwhelming lol 
    # Test range is 7 buckets with 400+ files 

    if wantToContine.lower() == "y" or "yes":
        response = s3Client.list_buckets()

        for bucket in response['Buckets']:

            # Create iterator for use in loop
            bucketTarget = bucket['Name']
            page_iterator = paginator.paginate(Bucket=bucketTarget)

            print()
            print("*********************")
            print("Searching Bucket: " + bucketTarget)
            print("*********************")
            print()
        
            # Loop
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:

                        targetFile = obj['Key']

                        response = s3Client.get_object(Bucket=bucketTarget, Key=targetFile)


                        # Read and decode the text content
                        # This gets Wonky
                        file_content = response['Body'].read().decode('utf-8',errors='ignore')



                        print()
                        print("*********************")
                        print("Searching KEYWORDS in : " + targetFile)
                        print("*********************")
                        print()

                        # Search Function For KeywordBank
                        for line in file_content.splitlines():
                            if re.search(keywordBank,line,re.IGNORECASE):

                                #Super dumb way to fix the huge output issue, will find better method later
                                # Still overwelms the terminal at a certain point. Might be worth to just export this all to a HTML file
                                if len(line) > 15:
                                    print("The output is way to large look for yourself")
                                else:
                                    print(line)

                        print()
                        print("*********************")
                        print("Searching PATTERNS in : " + targetFile)
                        print("*********************")
                        print()

                        for label, pattern in patternsBank.items():
                            for matchPattern in re.finditer(pattern,file_content):
                                print(label + ": " + matchPattern.group())

    print("That's all I found")



 

def s3ParanoidMode():

    sessionAWS = setAuth()
    s3Client = sessionAWS.client('s3')
    response = s3Client.list_buckets()
    bucketCount = 0
    
    for bucket in response['Buckets']:
        bucketCount += 1

    print()
    print("*********************")
    print("Total Buckets Found: " + str(bucketCount))
    print("*********************")
    print()



def s3WatchListMode():

    sessionAWS = setAuth()
    s3Client = sessionAWS.client('s3')
    response = s3Client.list_buckets()
    bucketCount = 0

    for bucket in response['Buckets']:
        bucketCount += 1

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
        "--kitchensink", action="store_true", help="Enable Kitchen Sink mode."
        )

    parser.add_argument(
        "--paranoid", action="store_true", help="Enable Paranoid mode."
        )

    parser.add_argument(
        "--watchlist", action="store_true", help="Enable watchlist mode."
        )


    args = parser.parse_args()
    
    if args.AWS_Service == "S3" and args.watchlist:
        print("Starting: " + args.AWS_Service + " Sniffer in WatchList Mode")
        s3WatchListMode()

    if args.AWS_Service == "S3" and args.kitchensink:
        print("Starting: " + args.AWS_Service + " Sniffer in Kitchen Sink Mode")
        s3KitchenSinkMode()

    if args.AWS_Service == "S3" and args.paranoid:
        print("Starting: " + args.AWS_Service + " Sniffer in Paranoid Mode")
        s3ParanoidMode()

# Main Function Loop
if __name__ == "__main__":
    main()

# TODO:
# Add recon mode that collects numerical data or recon switch on AWS resources? 

#s3 Glacier (Not sure how viable this will be)

#lambda Func
#lamdaObj = boto3.client('lambda')

#EFS Func

#FSx Func

#EBS Func

#MetaData Search Func?