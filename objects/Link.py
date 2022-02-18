import models
import settings
# code from Bart Meyers


class BS_BS_Link:
    def __init__(self, device1, device2):
        self.device1 = device1
        self.device2 = device2

        self.functional = 1
        pass

    def other(self, bs):
        if self.device1 is bs:
            return self.device2

        if self.device2 is bs:
            return self.device1

        return None

    def __str__(self):
        return "Link between {} and {}".format(self.device1, self.device2)


class UE_BS_Link:
    def __init__(self, ue, base_station, channel, power, dist, frequency):
        """
        :param ue:
        :param base_station:
        """
        self.ue = ue
        self.base_station = base_station
        self.power = power
        self.channel = channel
        self.distance = dist
        self.frequency = frequency

    @property
    def needed_bandwidth(self):
        """
        Calcculates needed bandwidth for this link based on the requested capacity and shannons capacity
        :return: the needed bandwidth
        """
        # TODO potential for division by 0
        return self.ue.requested_capacity / models.shannon_second_param(self.snr)

    @property
    def bandwidthneeded(self):
        """
        Calculates the bandwidth of a channel that is needed to satisfy the requested capacity of this link
        :return: smallest needed bandwidth chosen from settings.CHANNEL_BANDWIDTHS
        such that the full requested capacity is used
        """
        needed_bandwidth = settings.CHANNEL_BANDWIDTHS[0] # maximum bandwidth for a channel
        for bandwidth in settings.CHANNEL_BANDWIDTHS:
            if self.needed_bandwidth > bandwidth:
                break
            else:
                needed_bandwidth = bandwidth

        return needed_bandwidth

    @property
    def shannon_capacity(self):
        """
        Get the shannon capacity of the current connection
        :return:
        """
        return models.shannon_capacity(self.snr, self.base_station.get_bandwidth(self.ue))

    @property
    def snr(self):

        return models.snr(self.power)

    def __str__(self):
        return "Link between {} and {}".format(self.ue, self.base_station)
