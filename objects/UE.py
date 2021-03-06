import settings
# code from Bart Meyers

class UserEquipment:
    def __init__(self, id: int, x: float, y: float, rate_requirement: float, type: int):
        self.id = id
        self.x = x
        self.y = y
        self.height = settings.UE_HEIGHT
        self.rate_requirement = rate_requirement
        self.type = type

    def __str__(self):
        return "UE[{}], requested capacity: {}, x: {}, y: {}".format(self.id, self.rate_requirement, self.x, self.y)
