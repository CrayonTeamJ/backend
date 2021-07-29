import boto3
import os

s3 = boto3.resource(
    service_name = os.environ['s3_service_name'],
    region_name = os.environ['s3_region_name'],
    aws_access_key_id = os.environ['s3_aws_access_key_id'],
    aws_secret_access_key = os.environ['s3_aws_secret_access_key']
)

def upload_blob_file(file_dir, destination):
    s3.meta.client.upload_file(file_dir, 'crayon-team-j', destination)
    #s3.meta.client.upload_file('/Users/minwoong/Projects/Test/images/image.jpeg', 'teamj-data', 'image/image1.jpeg')