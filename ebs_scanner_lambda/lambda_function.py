import logging
import os

from datetime import datetime
from snapshots.snapshots import EBSSnapshots
from volumes.volumes import EBSVolumes
from s3client.s3_client import S3BucketClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)


RESULT_BUCKET_NAME = os.environ["RESULT_BUCKET_NAME"]
PATH_FORMAT = "%d_%m_%Y"
FILE_PREFIX = "%H_%M_%S"


def lambda_handler(event, context):
    ebs_snapshots = EBSSnapshots()
    ebs_volumes = EBSVolumes()

    s3_bucket_client = S3BucketClient(bucket_name=RESULT_BUCKET_NAME)

    data = {
        "unattached_ebs_volumes_size": ebs_volumes.get_size_of_unattached_volumes(),
        "unencrypted_ebs_volumes_size": ebs_volumes.get_size_of_unecnrypted_volumes(),
        "unencrypted_ebs_snapshots_size": ebs_snapshots.get_size_of_unencrypted_snapshots(),
    }

    today = datetime.now()
    formatted_path_prefix = today.strftime(PATH_FORMAT)
    formatted_file_prefix = today.strftime(FILE_PREFIX)
    path = "{}/{}.json".format(formatted_path_prefix, formatted_file_prefix)

    s3_bucket_client.write_json_data(path=path, body=data)
