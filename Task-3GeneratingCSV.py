from xmlrpc.client import boolean
import boto3
# Fetch account details using organizations api call 
aws = boto3.session.Session()# Logging into aws console
s3 = aws.client('s3', region_name= 'us-east-1') # Logging in the s3 console 
s3_res = boto3.resource('s3', region_name= 'us-east-1')
bucket_list = ['bhargavi_team-ww-s1', 'bhargavi_team-ww-s2', 'bhargavi_team-ww-s3', 'bhargavi_team-ww-s4', 'bhargavi_team-ww-s5', 'bhargavi_team-ww-s6', 'bhargavi_team-ww-s7', 'bhargavi_team-ww-s8', 'bhargavi_team-ww-s9', 'bhargavi_team-ww-s10']

#Creating Csv file and printing Colomn names
with open("s3_file4.csv","a") as f:
    print(f'bucket_name,bucket_size,public_status,versioning_status,bucket_region',file=f)

#looping for each bucket in bucket list 
for bucket in bucket_list:
    
    bucket_size = 0

    response = s3.list_objects(Bucket=bucket)['Contents']
    #fetching bucket Size

    for obj in response:

        bucket_size += obj['Size']
    # print(f'{bucket}: {bucket_size}')

    #fetching public or private status of Bucket
    public_status=boolean
    bucket_acl=s3.get_bucket_acl(Bucket=bucket)
    for grant in bucket_acl['Grants']:
        if grant['Grantee'].get('URI')=='http://acs.amazonaws.com/groups/global/AllUsers' or grant['Grantee'].get('URI')=='http://acs.amazonaws.com/groups/global/AuthenticatedUsers':
            public_private_status=True
            break
        else:
            public_private_status=False
        # print(public_status)
    
    #fetching versioning status of bucket
    versioning=s3_res.BucketVersioning(bucket)
    versioning_status=versioning.status
    # print(versioning_status)

    #fetching Bucket Region
    response=s3.get_bucket_location(Bucket=bucket)
    bucket_location=response['LocationConstraint']
    # print(bucket_location)

    #Generating Csv file with all status
    with open("s3_file4.csv", "a") as f:  
        print(f'{bucket},{bucket_size},{public_private_status},{versioning_status},{bucket_location}', file=f)




