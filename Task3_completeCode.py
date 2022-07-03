import boto3

# Fetch account details using organizations api call 
aws = boto3.session.Session() # Logging into aws console 
s3 = aws.client('s3', region_name= 'us-east-1') # Logging in the s3 console 
s3_res = boto3.resource('s3', region_name= 'us-east-1')

# Create a list of bucket name
numbers = range(1,11)

bucket_list = []
for i in numbers:
    string1 = 'bhargavi_india-ww-s-epam-xyz'
    string2 = str(i)
    bucket_list.append(string1 + string2)

print(bucket_list)

# 1. Create 10 S3 Buckets

for bucket in bucket_list:
    response = s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={
        'LocationConstraint': 'us-east-1'
    },)
    print(response)

# 2. Upload 100 MB+, 200MB+ , 300MB+ … data on each bucket

file1 = 'excelTeamWW.xlsx'
file2 = 'Script.docx'

for bucket in bucket_list:
    response1 = s3.upload_file('index.html', bucket,'data1')
    response2 = s3.upload_file('index.html', bucket, 'data2')

#  3. Make Sure any one bucket content is public, rest all are private
# Make bucket 1 content as public 

# Delete public access block for bucket 1:

response = s3.delete_public_access_block(
    Bucket=bucket_list[0]
)
print(response)


object_acl = s3_res.ObjectAcl(bucket_list[0],'data1')
response = object_acl.put(ACL='public-read') # ACL=public-read for public access

print(response)

# 4. Enable Versioning in bucket 1

versioning = s3_res.BucketVersioning(bucket_list[0])
versioning.enable()

# 5. Access logs enable for bucket 1

logging = s3.put_bucket_logging(Bucket=bucket_list[0],
                    BucketLoggingStatus={
                        'LoggingEnabled': {
                            'TargetBucket': bucket_list[1],
                            'TargetPrefix': 'accesslogsbucket1',
                            'TargetGrants': [
                            {
                            'Grantee': {
                            'Type': 'Group',
                            'URI': 'http://acs.amazonaws.com/groups/global/AllUsers',
                            },
                            'Permission': 'READ',
                },
            ],
                            }
                        },
                    )
print(logging)

