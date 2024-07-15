import logging
import boto3
import os
from botocore.exceptions import ClientError

BUCKET = os.environ.get("S3_BUCKET")

class S3Service:
    def upload_file(file_name, key, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3 = boto3.resource('s3')
        try:
            s3.Bucket(BUCKET).upload_fileobj(file_name, key, ExtraArgs={"ACL": "public-read"})
            uploaded_file_url = f"https://{BUCKET}.s3.amazonaws.com/{file_name}"
            return uploaded_file_url
        except ClientError as e:
            logging.error(e)     
            raise Exception(e)