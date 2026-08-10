<!-- ABOUT THE PROJECT -->
## AWS Secret Sniffer

This is part of my "rebuilding the tools I lost" project. This application will ask for AWS credentials and then based on your selection of target and method will start to pull and search for sensitive strings. 


## Getting Started

The format is:

```
awsSecretSniffer.py <target_AWS_StorageType> --METHOD
```

Currently this only supports S3 as an AWS storage type.

There are 3 methods.

--kitchsink
This searches all S3 Buckets and ALL files inside each S3 Bucket. 

--paranoid
Searches One target bucket, but then searches every file on said bucket. 

--watchlist
Searches only one bucket and one target file on said bucket. 

### Prerequisites

This tool only requires boto3, you can stand up an virtual environment or simply just install boto3 onto the machine. 
* pip
  ```sh
  pip install boto3
  ```





<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Roughly finish S3 prototype
- [ ] Add Lamda Search Functionality 
- [ ] Add recon methodolgy that lists how many storage types the current account has access too
- [] Add some error checking//user proofing
- [] Add reporting functionality (HTML//SQL Searchable)



<!-- CONTACT -->
## Contact

Ian Briley - [LinkedIn](https://www.linkedin.com/in/ian-briley)
<p align="right">(<a href="#readme-top">back to top</a>)</p>
