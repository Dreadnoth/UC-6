import boto3
from enum import Enum

from setup_logger import logger


class EC2ClientAllowedModes(Enum):
    SNAPSHOT = 1
    VOLUME = 2


class EC2Client:
    """
    Class that initializes boto EC2 client
    """

    FILTER_ENCRYPTED = {'Name': 'encrypted', 'Values': ['true']}
    FILTER_UNENCRYPTED = {'Name': 'encrypted', 'Values': ['false']}

    def __init__(self):
        self.ec2client = None
        try:
            self.ec2client = boto3.client('ec2')
        except Exception as e:
            logger.error(e)
            exit(1)

    def describe(self, mode=EC2ClientAllowedModes, filters=None):
        if filters is None:
            filters = []

        match mode:
            case EC2ClientAllowedModes.SNAPSHOT:
                return self.ec2client.describe_snapshots(Filters=filters, OwnerIds=["self"])
            case EC2ClientAllowedModes.VOLUME:
                return self.ec2client.describe_volumes(Filters=filters)
