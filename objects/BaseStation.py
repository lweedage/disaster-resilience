import math

import objects.Link as Link
import objects.City as City
import settings as settings
import util as util
import models as models
import random
# code from Bart Meyers


# TODO change mmwave workings
class BaseStation:
    def __init__(self, id, radio, x, y, height):
        self.id = id
        self.radio = radio
        self.y = float(y)
        self.x = float(x)
        self.height = float(height)

        self.connected_UE = dict()  # Dict(UE: Link)
        self.connected_BS = list()

        # self.minimum_band_needed = dict()

        self.channels = list()
        self.functional = 1

    def __str__(self):
        y = self.y
        x = self.x
        radio = str(self.radio)
        startmsg = f"Base station[{self.id}], {x=}, {y=}, {radio=}"
        for channel in self.channels:
            startmsg += "\n\t{}".format(str(channel))
        return startmsg

    def __repr__(self):
        return f"BS[{self.id}]: {self.x=},{self.y=},{self.radio=},#Channels={len(self.channels)}"

    def malfunction(self, new_functional):
        self.functional = new_functional
        self.create_new_channels()

    def add_link(self, link: Link.BS_BS_Link):
        self.connected_BS.append(link)

    def add_channel(self, frequency, power, angle):
        """
        Adds an omnidirectional channel to the basestation
        :param angle: The main direction in which the beam sends
        :param frequency: The frequency of the channel
        :param power: The transmit power for this channel
        :return: None
        """
        # Check if channel exist already
        # for c in self.channels:
        #     if c.frequency == frequency:
        #         return
        channel = Channel(frequency, power, angle, self)
        self.channels.append(channel)

    def __add__(self, other):
        new_link = Link.BS_BS_Link(self, other)
        self.connected_BS.append(new_link)
        other.add_link(new_link)
        return new_link

    def add_ue(self, ue, dist=None):
        """
        Adds a user connection to the basestation
        :param ue: user equipment to add
        :return: true if successful otherwise false
        """
        # Get best channel to add a device to
        best_channel = None
        best_prod = 0
        best_band_left = 0
        for channel in self.channels:
            if channel.can_connect(self, ue) and channel.productivity >= best_prod:
                if channel.band_left > best_band_left:
                    best_channel = channel
                    best_band_left = channel.band_left
                    best_prod = channel.productivity

        channel = best_channel
        if channel is None:  # No channels for the BS has bandwidth left
            return False

        # Calculate the power for the connection with the channel and create the link
        if dist is None:
            dist = util.distance_2d(self.x, self.y, ue.lon, ue.lat)
        params = models.ModelParameters(dist)
        params.distance_3d = util.distance_3d(self.height, ue.height, d2d=dist)
        params.ue_height = ue.height
        params.self_height = self.height
        params.area = self.area.area_type
        params.avg_building_height = self.area.avg_building_height
        params.avg_street_width = self.area.avg_street_width
        params.frequency = channel.frequency
        # TODO add beamforming model when needed
        power = models.received_power(self.radio, channel.power, params)
        if power < util.to_pwr(settings.MINIMUM_POWER):
            # print(f"power too low: {power=}; min power = {util.to_pwr(settings.MINIMUM_POWER)}")
            return False
        new_link = Link.UE_BS_Link(ue, self, channel, power, dist)
        channel_add = channel.add_device(ue, new_link.bandwidthneeded, self)
        # Additional test that should never trigger
        # if device failed to be added to the channel or the BS overflows revert and return False
        if not channel_add:
            print(f"Failed to add {ue=} to {channel=}")
            return False
        if self.overflow:
            print(f"Adding {ue=} to {channel=} cause bs overflow")
            del channel.devices[ue]
            del channel.desired_band[ue]
            return False
        self.connected_UE[ue] = new_link
        ue.set_base_station(new_link)
        return True

    @DeprecationWarning
    def direct_capacities(self):
        """
        DO NOT USE: DOES NOT DO Usefull stuff
        original use: redistribute connected ue over the channels
        :return:
        """
        self.create_new_channels()
        self.connected_UE = sorted(self.connected_UE, key=lambda x: x.link.bandwidthneeded, reverse=True)
        for UE in self.connected_UE:
            channel = max(self.channels, key=lambda c: (c.productivity, c.band_left))
            channel.add_device(UE, UE.link.bandwidthneeded, self)

    @property
    def overflow(self):
        for UE in self.connected_UE:
            if self.get_bandwidth(UE) == 0:
                return True

        return False

    def remove_ue(self, ue_link):
        del self.connected_UE[ue_link.ue]

    def get_bandwidth(self, ue):
        for channel in self.channels:
            bandwidth = channel.get_bandwidth(ue)
            if bandwidth is not None:
                return bandwidth
        return 0

    def create_new_channels(self):
        """
        Reecreates empty channels taking into account that channels can fail
        :return:
        """
        for channel in self.channels:
            channel.reset()
            if random.random() >= self.functional:
                channel.enabled = False

    def reset(self):
        self.functional = 1
        self.create_new_channels()
        self.connected_UE.clear()

    @DeprecationWarning
    def get_copy(self):
        new_bs = BaseStation(self.id, self.radio, self.lon, self.lat, self.height, self.area)


# TODO add method for reordering channel bandwidth
# TODO add method for determining if a user can connect if beamforming (due to similar angles)
class Channel:
    def __init__(self, frequency, power, bs, main_direction, enabled=True, beamforming=False):
        self.frequency = frequency
        self.power = power
        self.main_direction = main_direction

        self.devices = dict()
        self.desired_band = dict()

        self.beamforming: bool = beamforming
        self.used_angles = []

        self.bs = bs

        self.enabled = enabled
        self.max_devices = math.floor(settings.CHANNEL_BANDWIDTHS[0]
                                      / settings.CHANNEL_BANDWIDTHS[len(settings.CHANNEL_BANDWIDTHS) - 1])

    # TODO add angle to angles list if channel is mmWave
    def add_device(self, ue, minimum_bandwidth, bs):
        """
        Attempts to add new device to the channel
        :param ue:
        :param minimum_bandwidth:
        :return: True if successful otherwise False
        """
        # Check if device can be added
        if not self.can_connect(bs, ue):
            return False
        # Add device
        self.desired_band[ue] = minimum_bandwidth
        if self.beamforming:
            # If beamforming devices do not need to be reshuffeled.
            # If a device can be added for the angle it gets all bandwidth and is the only device within the angle
            self.devices[ue] = settings.CHANNEL_BANDWIDTHS[0]
            self.used_angles.append(util.get_angle(ue.lat, ue.lon, bs.lat, bs.lon))
            return True
        self.devices[ue] = minimum_bandwidth
        while self.band_left < 0:
            # Push device with maximum band down
            device = max(self.devices, key=lambda d: self.devices[d])
            stop_next = False
            new_band = None
            for i in settings.CHANNEL_BANDWIDTHS:
                if stop_next:
                    # enter here for a band lower than the band of the device
                    stop_next = False
                    new_band = i
                    break

                if self.devices[device] == i:
                    # Gets the current band for the device
                    stop_next = True

            if stop_next:
                # Could not push this device down a band
                # Should never be reached
                print("ERROR: Something within channel went horribly wrong")
                self.devices[device] = 0
                break

            self.devices[device] = new_band

        return True

    @property
    def band_left(self):
        if self.beamforming:
            # Beamforming has one beam per user with the full bandwidth available (for each angle).
            return settings.CHANNEL_BANDWIDTHS[0]
        return settings.CHANNEL_BANDWIDTHS[0] - sum([self.devices[d] for d in self.devices])

    def has_band_left(self):
        if self.beamforming:
            return self.enabled
        return self.enabled and len(self.devices) < self.max_devices

    @property
    def connected_devices(self):
        return len(self.devices)

    @property
    def productivity(self):
        if len(self.devices) == 0:
            return 1
        return min(sum(self.devices.values()) / sum(self.desired_band.values()), 1)

    def __str__(self):
        msg = "Channel[{}]:".format(self.frequency)
        for device in self.devices:
            msg += "\n{} Desired Bandwidth:{}, Actual Bandwidth:{}".format(device, self.desired_band[device],
                                                                           self.devices[device])
        return msg

    def __repr__(self):
        return f"Channel[{self.frequency}]: {self.enabled=}; #devices = {len(self.devices)}; power = {self.power} "

    def __eq__(self, other):
        if not isinstance(other, Channel):
            raise TypeError
        return self.frequency == other.frequency

    def get_bandwidth(self, ue):
        if ue not in self.devices:
            return None

        return self.devices[ue]

    def reset(self):
        self.devices.clear()
        self.desired_band.clear()
        self.used_angles.clear()

    def can_connect(self, bs, ue):
        """
        Determines if a user can connect
        :param bs:
        :param ue:
        :return:
        """
        if not self.enabled:
            return False
        if self.beamforming:
            # determine if the angle (with some margin) is already in use
            # if not ue can connect otherwise not
            angle = util.get_angle(ue.lat, ue.lon, bs.lat, bs.lon)
            for used_angle in self.used_angles:
                if used_angle - settings.BEAMFORMING_CLEARANCE / 2 <= angle <= used_angle + settings.BEAMFORMING_CLEARANCE / 2:
                    return False
        else:
            return self.has_band_left()
        return True
