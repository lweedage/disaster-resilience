import numpy as np
import scipy.sparse

import util as util


class Parameters:
    def __init__(self, seed, zip_codes, provider_list, percentage, buffer_size, city_list=None, province=None,
                 delta=None, radius_disaster=0, random_failure=0, user_increase=0, capacity_distribution=False,
                 geographic_failure=False, back_up = False):

        self.back_up = back_up
        if back_up:
            provider_list = ['KPN', 'T-Mobile', 'Vodafone']

        self.zip_codes = zip_codes
        self.number_of_bs = int()
        self.number_of_users = int()
        self.number_of_channels = int()
        self.percentage = percentage
        self.providers = provider_list
        self.seed = seed
        self.percentage = percentage

        self.region = None
        self.zip_code_region = None
        self.center = None
        self.radius_disaster = radius_disaster
        self.random_failure = random_failure
        self.user_increase = user_increase
        self.capacity_distribution = capacity_distribution
        self.geographic_failure = geographic_failure

        if province:
            self.cities = util.find_cities(province)
            self.city_name = province
        elif city_list is None:
            self.cities = util.find_cities('Netherlands')
            self.city_name = 'Netherlands'
        else:
            self.cities = city_list
            self.city_name = city_list[0]

        self.percentages = {'KPN': 0.4, 'T-Mobile': 0.4, 'Vodafone': 0.2}

        if len(provider_list) == 1:
            provider = provider_list[0]
            percentage_MNO = self.percentages[provider]

        else:
            provider = 'all_MNOs'
            percentage_MNO = 1

        self.provider = provider

        self.filename = f'{self.city_name}{provider}{percentage}{str(percentage_MNO)[:4]}'
        self.bsfilename = f'{self.city_name}{provider}'
        self.filename_noMNO = f'{self.city_name}'
        self.userfilename = self.filename

        if delta:
            self.userfilename = f'{self.city_name}{provider}{percentage}{str(percentage_MNO)[:4]}{delta}'
            self.filename = self.userfilename

        if radius_disaster != 0:
            self.filename += f'disaster{radius_disaster}'
            self.bsfilename += f'disaster{radius_disaster}'

        if random_failure != 0:
            self.filename += f'random{random_failure}'
            self.bsfilename += f'random{random_failure}'

        if user_increase != 0:
            self.userfilename += f'user_increase{user_increase}'
            self.filename += f'user_increase{user_increase}'

        if capacity_distribution:
            self.userfilename += 'capacity_ecdf'
            self.filename += 'capacity_ecdf'

        if geographic_failure:
            self.filename += 'geographic_failure'
            self.bsfilename += 'geographic_failure'

        if back_up:
            self.filename += 'backup'
            self.userfilename += 'backup'

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

        self.percentage_plus_MNO = percentage_MNO * percentage * (1 + user_increase / 100)

        self.delta = delta

        self.path_loss = None

        self.buffer_size = buffer_size

        self.failed_BS = None
        self.failed_BS_coords = None

    def initialize(self):
        np.random.seed(self.seed)

        self.los_probabilities = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs))
        self.fading4 = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs))
        self.fading6 = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs))
        self.fading78 = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs))
        self.fading8 = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs))

        self.path_loss = dict()
        self.interference = dict()

        for freq in self.all_freqs:
            self.path_loss[freq] = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs))
            self.interference[freq] = scipy.sparse.lil_matrix((self.number_of_users, self.number_of_bs))

    def failure_update(self, failed_bs):
        self.filename += f'failure_{failed_bs}'
        self.bsfilename += f'failure_{failed_bs}'
        self.failed_BS = failed_bs
        self.failed_BS_coords = (self.BaseStations[failed_bs].x, self.BaseStations[failed_bs].y)
