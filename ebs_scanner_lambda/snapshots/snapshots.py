from ec2client.ec2_client import EC2Client, EC2ClientAllowedModes


class EBSSnapshots(EC2Client):
    """
    Class for handling EBS Snapshots information
    """

    def __init__(self):
        super().__init__()
        self.__snapshot_key = "Snapshots"

    def __describe_snapshots(self, filters=None):
        return super().describe(mode=EC2ClientAllowedModes.SNAPSHOT, filters=filters)

    def get_size_of_unencrypted_snapshots(self):
        filters = [self.FILTER_UNENCRYPTED]
        result = self.__describe_snapshots(filters=filters)

        gigabytes = 0

        if result is None or self.__snapshot_key not in result:
            return gigabytes

        snapshots = result[self.__snapshot_key]

        for snapshot in snapshots:
            gigabytes += snapshot['VolumeSize']

        return gigabytes