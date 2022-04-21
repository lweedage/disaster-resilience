import math
import settings as settings
import util as util
import models as models
import random
import numpy as np


# code from Bart Meyers

class BaseStation:
    def __init__(self, id, radio, x, y, provider='', small_cell=False):
        self.id = id
        self.radio = radio
        self.y = float(y)
        self.x = float(x)
        self.small_cell = bool(small_cell)
        self.provider = str(provider)

        self.channels = list()
        self.interferers = list()
        self.area_type = util.AreaType
        self.frequencies = set()

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

    def add_channel(self, id, BS_id, height, frequency, power, angle, bandwidth):
        """
        Adds an omnidirectional channel to the basestation
        :param bandwidth:
        :param height: The height of the base station
        :param angle: The main direction in which the beam sends
        :param frequency: The frequency of the channel
        :param power: The transmit power for this channel (Effective Radiated Power, in dBW)
        :return: None
        """
        channel = Channel(id, BS_id, height, frequency, power, angle, bandwidth, beamwidth=360)
        self.channels.append(channel)


class Channel:
    def __init__(self, id, BS_id, height, frequency, power, main_direction, bandwidth, beamwidth=360):
        self.id = id
        self.BS_id = BS_id
        self.height = height
        self.frequency = frequency
        self.power = power
        self.main_direction = main_direction
        self.bandwidth = bandwidth
        self.beamwidth = beamwidth

        self.users = list()
        self.bs_interferers = list()

    @property
    def connected_users(self):
        return len(self.users)

    def add_user(self, user):
        self.users.append(user)

    def find_interferers(self, p):
        self_bs = p.BaseStations[self.BS_id]
        interferers = list()
        interference_levels = list()
        for bs in p.BaseStations:
            if bs != self_bs:
                if self.frequency in bs.frequencies:
                    if 0 < util.distance_2d(bs.x, bs.y, self_bs.x,
                                            self_bs.y) < 10000:  # TODO ASSUMPTION that only interferers within 10km radius can interfere
                        interference_level = models.highest_snr(bs, self_bs, [i for i in bs.channels if
                                                                                        i.frequency == self.frequency], p)
                        interferers.append(bs.id)
                        interference_levels.append(interference_level)
        if settings.CUTOFF_VALUE_INTERFERENCE == 0:
            self.bs_interferers = interferers
        else:
            indices = np.argsort(interference_levels)[:-settings.CUTOFF_VALUE_INTERFERENCE]
            self.bs_interferers = [p.BaseStations[interferers[i]] for i in indices]
