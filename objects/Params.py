import util as util
import numpy as np


class Parameters:
    def __init__(self, seed, zip_codes, provider_list, percentage, city_list=None, province=None):
        self.zip_codes = zip_codes
        self.number_of_bs = int()
        self.number_of_users = int()
        self.percentage = percentage
        self.providers = provider_list
        self.seed = seed

        self.region = None
        self.zip_code_region = None

        if province:
            self.cities = util.find_cities(province)
            city_name = province
        elif city_list is None:
            self.cities = None
            city_name = 'Netherlands'
        else:
            self.cities = city_list
            city_name = city_list[0]

        if len(provider_list) == 1:
            provider = provider_list[0]
        else:
            provider = 'all_MNOs'

        self.filename = f'{city_name}{provider}{percentage}'

        self.los_probabilities = None
        self.fading4 = None
        self.fading6 = None
        self.fading78 = None
        self.fading8 = None

        self.xbs = list()
        self.ybs = list()
        self.BaseStations = list()

        self.x_user = list()
        self.y_user = list()
        self.users = list()

    def initialize(self):
        np.random.seed(self.seed)
        self.los_probabilities = np.random.uniform(0, 1, (self.number_of_users, self.number_of_bs))
        self.fading4 = np.random.normal(0, 4, (self.number_of_users, self.number_of_bs))
        self.fading6 = np.random.normal(0, 6, (self.number_of_users, self.number_of_bs))
        self.fading78 = np.random.normal(0, 7.8, (self.number_of_users, self.number_of_bs))
        self.fading8 = np.random.normal(0, 8, (self.number_of_users, self.number_of_bs))
        print(self.fading4)