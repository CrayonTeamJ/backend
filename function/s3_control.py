import boto3


def upload_blob_file(file_dir, destination):
    s3.meta.client.upload_file(file_dir, 'crayon-team-j', destination)
    #s3.meta.client.upload_file('/Users/minwoong/Projects/Test/images/image.jpeg', 'teamj-data', 'image/image1.jpeg')