import boto3

s3 = boto3.resource(
    service_name='s3',
    region_name='ap-northeast-2',
    aws_access_key_id="AKIA5HOZ5LMZNE2DBDBU",
    aws_secret_access_key = "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"
)

def upload_blob_file(file_dir, destination):
    s3.meta.client.upload_file(file_dir, 'crayon-team-j', destination)
    #s3.meta.client.upload_file('/Users/minwoong/Projects/Test/images/image.jpeg', 'teamj-data', 'image/image1.jpeg')