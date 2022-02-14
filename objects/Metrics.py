import util
# code from Bart Meyers


class Metrics:
    def __init__(self):
        self.isolated_users = []
        self.received_service = []
        self.received_service_half = []
        self.avg_distance = []
        self.isolated_systems = []
        self.active_base_stations = []
        self.snr = []
        self.connectedUE_BS = []
        self.active_channels = []

    def add_metric(self, metrics):
        self.isolated_users.append(metrics[0])

        self.received_service.append(metrics[1])

        self.received_service_half.append(metrics[2])

        self.avg_distance.append(metrics[3])

        self.isolated_systems.append(metrics[4])

        self.active_base_stations.append(metrics[5])

        self.snr.append(metrics[6])

        self.connectedUE_BS.append(metrics[7])

        self.active_channels.append(metrics[8])

    def get_metrics(self):
        return util.avg(self.isolated_users), \
               util.avg(self.received_service), \
               util.avg(self.received_service_half), \
               util.avg(self.avg_distance), \
               util.avg(self.isolated_systems), \
               util.avg(self.active_base_stations), \
               util.avg(self.snr), \
               util.avg(self.connectedUE_BS), \
               util.avg(self.active_channels)

    def get_cdf(self):
        return util.cdf(self.isolated_users), \
               util.cdf(self.received_service), \
               util.cdf(self.received_service_half), \
               util.cdf(self.avg_distance), \
               util.cdf(self.isolated_systems), \
               util.cdf(self.active_base_stations), \
               util.cdf(self.snr), \
               util.cdf(self.connectedUE_BS), \
               util.cdf(self.active_channels)

    def add_metrics_object(self, metric):
        self.isolated_users = self.isolated_users + metric.isolated_users
        self.received_service = self.received_service + metric.received_service
        self.received_service_half = self.received_service_half + metric.received_service_half
        self.avg_distance = self.avg_distance + metric.avg_distance
        self.isolated_systems = self.isolated_systems + metric.isolated_systems
        self.active_base_stations = self.active_base_stations + metric.active_base_stations
        self.snr = self.snr + metric.snr
        self.connectedUE_BS = self.connectedUE_BS + metric.connectedUE_BS
        self.active_channels = self.active_channels + metric.active_channels

    def csv_export(self):
        res = []
        for i in range(len(self.isolated_users)):
            res.append([self.isolated_users[i],
                        self.received_service[i],
                        self.received_service_half[i],
                        self.avg_distance[i],
                        self.isolated_systems[i],
                        self.active_base_stations[i],
                        self.snr[i],
                        self.connectedUE_BS[i],
                        self.active_channels[i]])

        return res

    def __str__(self):
        return "({},{},{},{},{},{},{},{},{})".format(util.avg(self.isolated_users),
                                                     util.avg(self.received_service),
                                                     util.avg(self.received_service_half),
                                                     util.avg(self.avg_distance),
                                                     util.avg(self.isolated_systems),
                                                     util.avg(self.active_base_stations),
                                                     util.avg(self.snr),
                                                     util.avg(self.connectedUE_BS),
                                                     util.avg(self.active_channels))
