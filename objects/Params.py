import scipy.sparse

import util as util
import numpy as np

class Parameters:
    def __init__(self, seed, zip_codes, provider_list, percentage, city_list=None, province=None, delta = None, rain = None, radius_disaster = 0, random_failure = 0, user_increase = 0):
        self.zip_codes = zip_codes
        self.number_of_bs = int()
        self.number_of_users = int()
        self.number_of_channels = int()
        self.percentage = percentage
        self.providers = provider_list
        self.seed = seed

        self.region = None
        self.zip_code_region = None
        self.center = None
        self.rain = rain
        self.radius_disaster = radius_disaster
        self.random_failure = random_failure
        self.user_increase = user_increase

        if province:
            self.cities = util.find_cities(province)
            self.city_name = province
        elif city_list is None:
            self.cities = util.find_cities('Netherlands')
            self.city_name = 'Netherlands'
        else:
            self.cities = city_list
            self.city_name = city_list[0]

        if len(provider_list) == 1:
            provider = provider_list[0]
            if provider == 'KPN':
                percentage_MNO = 1/3
            elif provider == 'T-Mobile':
                percentage_MNO = 1/3
            else:
                percentage_MNO = 1/3
        else:
            provider = 'all_MNOs'
            percentage_MNO = 1

        self.provider = provider

        self.filename = f'{self.city_name}{provider}{percentage}{percentage_MNO}'
        self.bsfilename = f'{self.city_name}{provider}'
        self.filename_noMNO = f'{self.city_name}'
        self.userfilename = self.filename

        if delta:
            self.userfilename = f'{self.city_name}{provider}{percentage}{percentage_MNO}{delta}'
            self.filename = self.userfilename

        if rain:
            self.filename += f'rain{rain}'

        if radius_disaster != 0:
            self.filename += f'disaster{radius_disaster}'
            self.bsfilename += f'disaster{radius_disaster}'

        if random_failure != 0:
            self.filename += f'random{random_failure}'
            self.bsfilename += f'random{random_failure}'

        if user_increase != 0:
            self.userfilename += f'user_increase{user_increase}'
            self.filename += f'user_increase{user_increase}'

        self.los_probabilities = None
        self.fading4 = None
        self.fading6 = None
        self.fading78 = None
        self.fading8 = None

        self.xbs = list()
        self.ybs = list()
        self.BaseStations = list()
        self.all_freqs = list()

        self.x_user = list()
        self.y_user = list()
        self.users = list()

        self.percentage_plus_MNO = percentage_MNO * percentage

        self.delta = delta

        self.path_loss = None

    def initialize(self):
        np.random.seed(self.seed)

        # size = max(self.number_of_users, self.number_of_bs)
        self.los_probabilities = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs)) #np.random.uniform(0, 1, (self.number_of_users, self.number_of_bs))
        self.fading4 = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs)) #np.random.normal(0, 4, (self.number_of_users, self.number_of_bs))
        self.fading6 = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs)) #np.random.normal(0, 6, (self.number_of_users, self.number_of_bs))
        self.fading78 = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs)) #np.random.normal(0, 7.8, (self.number_of_users, self.number_of_bs))
        self.fading8 = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs)) #np.random.normal(0, 8, (self.number_of_users, self.number_of_bs))


        self.path_loss = dict()
        self.interference = dict()

        for freq in self.all_freqs:
            self.path_loss[freq] = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs))
            self.interference[freq] = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs))
