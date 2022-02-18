from objects.Link import UE_BS_Link
import settings
# code from Bart Meyers

class UserEquipment:
    def __init__(self, id: int, x: float, y: float, rate_requirement: float):
        self.id = id
        self.rate_requirement = rate_requirement
        self.x = x
        self.y = y
        self.link = None
        self.height = settings.UE_HEIGHT

    def set_base_station(self, link: UE_BS_Link):
        self.link = link

    @property
    def snr(self):
        return self.link.snr

    def __str__(self):
        return "UE[{}], requested capacity: {}, x: {}, y: {}".format(self.id, self.rate_requirement, self.x, self.y)

    def reset(self):
        self.link = None
