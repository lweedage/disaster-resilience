import dataclasses

from settings import ACTIVITY
import util as util
import settings as settings


@dataclasses.dataclass
class Area:
    min_lat: float
    min_lon: float
    max_lat: float
    max_lon: float
    area_type: util.AreaType = util.AreaType.UMA
    avg_building_height: float = settings.AVG_BUILDING_HEIGHT
    avg_street_width: float = settings.AVG_STREET_WIDTH


class City:
    def __init__(self, name, min_lat, min_lon, max_lat, max_lon, population):
        self.name = name
        self.min_lat = float(min_lat)
        self.min_lon = float(min_lon)
        self.max_lat = float(max_lat)
        self.max_lon = float(max_lon)
        # Areas in the city
        self.umi_area = None
        self.uma_area = None
        self.rma_area = None
        self.areas_defined = False
        self.population = int(population)
        self.active_users = int((ACTIVITY * self.population) // 1)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s(name=%r, population=%r, active_users=%r, min_lat=%r, max_lat=%r, min_lon=%r, max_lon=%r)" \
               % (self.__class__, self.name, self.population, self.active_users,
                  self.min_lat, self.max_lat, self.min_lon, self.max_lon)

    def area(self, lon, lat):
        """
        Returns the area of a location
        :param lon: lon of the location
        :param lat: lat of the location
        :return: The area the location (lon,lat) is in
        """
        # If area exists
        if self.umi_area is not None:
            # If location within border
            if self.umi_area.min_lon <= lon <= self.umi_area.max_lon \
                    and self.umi_area.min_lat <= lat <= self.umi_area.max_lat:
                return self.umi_area
        if self.uma_area is not None:
            if self.uma_area.min_lon <= lon <= self.uma_area.max_lon \
                    and self.uma_area.min_lat <= lat <= self.uma_area.max_lat:
                return self.uma_area
        if self.rma_area is not None:
            if self.rma_area.min_lon <= lon <= self.rma_area.max_lon \
                    and self.rma_area.min_lat <= lat <= self.rma_area.max_lat:
                return self.rma_area
