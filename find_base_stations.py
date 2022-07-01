import json
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union
import objects.BaseStation as BSO
import util
from settings import *
import sys
import progressbar

sys.setrecursionlimit(100000)

# code adapted from Bart Meyers

def find_zip_code_region(params):
    zip_code_region_data = util.from_data(f'data/BSs/{params.filename_noMNO}zip_code_region_data.p')
    region = util.from_data(f'data/BSs/{params.filename_noMNO}region.p')
    zip_codes = params.zip_codes
    if zip_code_region_data is None:
        if isinstance(params.cities[0], int):
            zip_code_region_data = zip_codes[zip_codes['postcode'].isin(params.cities)]
        else:
            zip_code_region_data = zip_codes[zip_codes['municipali'].isin(params.cities)]
        region = gpd.GeoSeries(unary_union(zip_code_region_data['geometry']))

        util.to_data(zip_code_region_data, f'data/BSs/{params.filename_noMNO}zip_code_region_data.p')
        util.to_data(region, f'data/BSs/{params.filename_noMNO}region.p')
    params.region = region
    params.zip_code_region = zip_code_region_data
    params.center = region.centroid[0]
    return params


def load_bs(params):
    UMA = gpd.GeoSeries(unary_union(params.zip_code_region[params.zip_code_region['scenario'] == 'UMa'].geometry))
    RMA = gpd.GeoSeries(unary_union(params.zip_code_region[params.zip_code_region['scenario'] == 'RMa'].geometry))
    all_basestations = util.from_data(f'data/BSs/{params.bsfilename}_all_basestations.p')
    xs = util.from_data(f'data/BSs/{params.bsfilename}_xs.p')
    ys = util.from_data(f'data/BSs/{params.bsfilename}_ys.p')
    channel_count = util.from_data(f'data/BSs/{params.bsfilename}_channels.p')
    all_freqs = util.from_data(f'data/BSs/{params.bsfilename}_all_freqs.p')

    # all_basestations = None
    if all_basestations is None:
        print('BSs are not stored in memory')
        all_basestations = list()
        id = 0
        xs, ys = [], []
        all_freqs = set()
        channel_count = 0

        LTE, NR, UMTS = 0, 0, 0
        with open(BS_PATH) as f:
            bss = json.load(f)
            bar = progressbar.ProgressBar(maxval=len(bss),
                                          widgets=[progressbar.Bar('=', f'Finding BSs {params.bsfilename} [', ']'), ' ',
                                                   progressbar.Percentage(), ' ', progressbar.ETA()])
            bar.start()

            # Loop over base stations
            for key, index in zip(bss.keys(), range(len(bss))):
                bar.update(index)
                # small_cell = False
                bs = bss[key]
                x = float(bs.get('x'))
                y = float(bs.get('y'))
                if params.region.contains(Point(x, y)).bool() and Point(x,y).distance(params.center) > params.radius_disaster:
                    Continue = True
                    if bs.get("type") == "LTE":
                        radio = util.BaseStationRadioType.LTE

                    elif bs.get("type") == "5G NR":
                        radio = util.BaseStationRadioType.NR
                    elif bs.get("type") == "UMTS":
                        radio = util.BaseStationRadioType.UMTS
                    elif bs.get("type") == "GSM":
                        radio = util.BaseStationRadioType.GSM
                        Continue = False
                    else:
                        print(bs.get("HOOFDSOORT"))  # there are no other kinds of BSs in this data set

                    if Continue:
                        new_bs = BSO.BaseStation(id, radio, x, y)
                        channel = 0
                        for key in bs.get("antennas").keys():
                            antenna = bs.get("antennas").get(key)
                            frequency = antenna.get("frequency")
                            provider, bandwidth = util.find_provider(frequency / 1e6)
                            if provider in params.providers:
                                all_freqs.add(frequency)
                                main_direction = antenna.get('angle')
                                if main_direction != 'Omnidirectional':  # we only consider three-sectorized antenna's
                                    # if bs.get("type") == "LTE":
                                    #     LTE += 1
                                    # elif bs.get("type") == "5G NR":
                                    #     NR += 1
                                    # elif bs.get("type") == "UMTS":
                                    #     UMTS += 1

                                    power = POWER_PERCENTAGE * (antenna.get("power") + 30)#We convert ERP power in dBW to dBm
                                    height = bs.get('antennas')[str(0)].get("height")

                                    new_bs.add_channel(key, new_bs.id, height, frequency, power, main_direction,
                                                       bandwidth)
                                    new_bs.frequencies.add(frequency)
                                    channel += 1

                            # if channel > 0 and provider in params.providers:
                            #     powers = [channel.power for channel in new_bs.channels]
                            #     if max(powers) <= 17.8 + 30:  # 17.8 dBW is 60 W, that is the maximum power of a small cell.
                            #         small_cell = True

                        if channel > 0:
                            if UMA.contains(Point(x, y)).bool():
                                area_type = util.AreaType.UMA
                            elif RMA.contains(
                                    Point(x, y)).bool():
                                area_type = util.AreaType.RMA
                            else:
                                print('No type', x, y)

                            # if small_cell:
                            #     area_type = util.AreaType.UMI

                            new_bs.area_type = area_type

                            p = np.random.uniform(0, 1)
                            if p >= params.random_failure:
                                all_basestations.append(new_bs)
                                xs.append(x)
                                ys.append(y)
                                id += 1
            # bar.finish()
        params.xbs = xs
        params.ybs = ys
        params.BaseStations = all_basestations
        params.number_of_bs = len(all_basestations)


        freq_channels = dict()
        channel_count = 0
        for bs in all_basestations:
            for channel in bs.channels:
                channel_count += 1
                if channel.frequency in freq_channels.keys():
                    freq_channels[channel.frequency].add(channel.BS_id)
                else:
                    freq_channels[channel.frequency] = {channel.BS_id}
        for bs in all_basestations:
            for channel in bs.channels:
                channel.bs_interferers = [params.BaseStations[i] for i in freq_channels[channel.frequency] if
                                          i != channel.BS_id and util.distance_2d(params.BaseStations[i].x, params.BaseStations[i].y, bs.x, bs.y) <= 5_000]

        util.to_data(all_basestations, f'data/BSs/{params.bsfilename}_all_basestations.p')
        util.to_data(xs, f'data/BSs/{params.bsfilename}_xs.p')
        util.to_data(ys, f'data/BSs/{params.bsfilename}_ys.p')
        util.to_data(channel_count, f'data/BSs/{params.bsfilename}_channels.p')
        util.to_data(all_freqs, f'data/BSs/{params.bsfilename}_all_freqs.p')

        params.all_freqs = list(all_freqs)
        params.number_of_channels = channel_count
        params.initialize()
    else:
        params.xbs = xs
        params.ybs = ys
        params.BaseStations = all_basestations
        params.number_of_bs = len(all_basestations)
        params.number_of_channels = channel_count
        params.all_freqs = list(all_freqs)
        params.initialize()
    return params
    # print(f'UMTS: {UMTS}, LTE: {LTE}, NR: {NR}')
