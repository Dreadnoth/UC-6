import json

import boto3

from setup_logger import logger


class S3BucketClient:

    def __init__(self, bucket_name):
        self.s3client = None
        self.s3bucket = bucket_name
        try:
            self.s3client = boto3.client('s3')
        except Exception as e:
            logger.error(e)
            exit(1)

    def write_json_data(self, path, body):
        try:
            self.s3client.put_object(
                Body=json.dumps(body),
                Bucket=self.s3bucket,
                Key=path
            )
        except Exception as e:
            logger.error(e)
