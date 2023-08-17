from ec2client.ec2_client import EC2Client, EC2ClientAllowedModes


class EBSVolumes(EC2Client):
    """
    Class for handling EBS Volumes information
    """

    def __init__(self):
        super().__init__()
        self.__volume_key = "Volumes"

    def __describe_volumes(self, filters=None):
        return super().describe(mode=EC2ClientAllowedModes.VOLUME, filters=filters)

    def __get_unattached_volumes(self, volumes):
        return filter(lambda volume: not volume['Attachments'], volumes)

    def get_size_of_unattached_volumes(self):
        result = self.__describe_volumes()  # get all volumes

        gigabytes = 0

        if result is None or self.__volume_key not in result:
            return gigabytes

        volumes = result[self.__volume_key]
        unattached_volumes = self.__get_unattached_volumes(volumes=volumes)

        for unattached_volume in unattached_volumes:
            gigabytes += unattached_volume['Size']

        return gigabytes

    def get_size_of_unecnrypted_volumes(self):
        filters = [self.FILTER_UNENCRYPTED]
        result = self.__describe_volumes(filters=filters)  # get all volumes

        gigabytes = 0

        if result is None or self.__volume_key not in result:
            return gigabytes

        volumes = result[self.__volume_key]

        for volume in volumes:
            gigabytes += volume['Size']

        return gigabytes
