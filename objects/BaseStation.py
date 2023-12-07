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
    def __init__(self, id, BS_id, height, frequency, power, main_direction, bandwidth,  beamwidth=360):
        self.id = id
        self.BS_id = BS_id
        self.height = height
        self.frequency = frequency
        self.power = power # Can be changed according to the load
        self.max_power = power # Should not be changed
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

    def clear_users(self):
        self.users = list()

    def update_power(self, power_in_W):
        if power_in_W <= 0:
            if power_in_W < 0:
                print(f"Failed to update channel {self.id} from BS {self.BS_id} with negative power ({power_in_W} W), fallback to 0 W (-inf dB).")
            self.power = float('-inf')
        elif util.to_db(power_in_W) <= self.max_power: # if the power is in the correct range, update it.
            self.power = util.to_db(power_in_W)
        else:
            print(f"Failed to update channel {self.id} power from BS {self.BS_id}, fallback to max_power.")
            self.power = self.max_power
