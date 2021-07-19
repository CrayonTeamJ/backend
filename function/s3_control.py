import boto3

s3 = boto3.resource(
    service_name='s3',
    region_name='ap-northeast-2',
    aws_access_key_id="AKIAQ6LTZG4D2NMGBMQJ",
    aws_secret_access_key = "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"
)

def upload_blob_file(file_dir, destination):
    s3.meta.client.upload_file(file_dir, 'teamj-data', destination)
    #s3.meta.client.upload_file('/Users/minwoong/Projects/Test/images/image.jpeg', 'teamj-data', 'image/image1.jpeg')