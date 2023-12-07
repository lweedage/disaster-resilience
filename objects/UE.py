import settings
# import math
# code from Bart Meyers

class UserEquipment:
    def __init__(self, id: int, x: float, y: float, rate_requirement: float):
        self.id = id
        self.x = x
        self.y = y
        self.height = settings.UE_HEIGHT
        self.rate_requirement = rate_requirement
        self.provider = ''
        # self.connection = UserConnection()

    """ @property
    def connected(self):
        return self.connection.SINR is not None and self.SINR >= (settings.MINIMUM_SNR - settings.PRECISION_MARGIN)
    
    @property
    def satisfied(self):
        return self.connection.effectiveBW is not None and self.connection.effectiveBW*math.log2(1+self.connection.SINR) >= (self.rate_requirement - settings.PRECISION_MARGIN) """

    def __str__(self):
        return "UE[{}], requested capacity: {}, x: {}, y: {}".format(self.id, self.rate_requirement, self.x, self.y)

# TODO: add user connection with info of the current connection to avoid saving different structures to the connections.
""" class UserConnection:
    def __init__(self, provider=None, BS_id=None, channel_id=None, SINR=None, SNR=None, effectiveBW=None):
        self.provider = provider
        self.SINR = SINR
        self.SNR = SNR       
        self.BS_id = BS_id 
        self.channel_id = channel_id
        self.effectiveBW = effectiveBW # fraction of time x BW

    def update_connection(self, provider, BS_id, channel_id, SINR, SNR, effectiveBW):
        self.provider = provider
        self.SINR = SINR
        self.SNR = SNR       
        self.BS_id = BS_id 
        self.channel_id = channel_id
        self.effectiveBW = effectiveBW """