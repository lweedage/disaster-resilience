from objects.Link import UE_BS_Link
import settings

class UserEquipment:
    def __init__(self, id: int, lon: float, lat: float, capacity: int):
        self.id = id
        self.requested_capacity = capacity
        self.lon = lon
        self.lat = lat
        self.link = None
        self.height = settings.UE_HEIGHT

    def set_base_station(self, link: UE_BS_Link):
        self.link = link

    @property
    def snr(self):
        return self.link.snr

    def __str__(self):
        return "UE[{}], requested capacity: {}, lon: {}, lat: {}".format(self.id, self.requested_capacity, self.lon, self.lat)

    def reset(self):
        self.link = None
