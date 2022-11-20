import geopandas as gpd
from shapely.ops import unary_union

import collect_base_stations
import objects.Params as p
from util import *

zip_codes = gpd.read_file('zip_codes.shp')

for i, row in zip_codes.iterrows():
    print(i, 'out of', len(zip_codes))
    GSM, UMTS, LTE, NR = 0, 0, 0, 0
    region = gpd.GeoSeries(unary_union(row['geometry']))
    mno = ['KPN', 'T-Mobile', 'Vodafone']
    percentage = 1
    seed = 1

    params = p.Parameters(seed, zip_codes, mno, percentage, buffer_size=2000, city_list=None, province=None)
    params.zip_code_region = row
    params.region = region
    params = collect_base_stations.load_bs(params)

    for BS in params.BaseStations:
        if BS.radio == BaseStationRadioType.GSM:
            GSM += 1
        elif BS.radio == BaseStationRadioType.UMTS:
            UMTS += 1
        elif BS.radio == BaseStationRadioType.LTE:
            LTE += 1
        elif BS.radio == BaseStationRadioType.NR:
            NR += 1

    zip_codes.at[i, 'GSM_BS'] = GSM
    zip_codes.at[i, 'UMTS_BS'] = UMTS
    zip_codes.at[i, 'LTE_BS'] = LTE
    zip_codes.at[i, 'NR_BS'] = NR
    zip_codes.at[i, 'BSs'] = UMTS + LTE + NR

zip_codes['BS_density'] = zip_codes['BSs'] / zip_codes['geometry'].area

for i, row in zip_codes.iterrows():
    if zip_codes.at[i, 'stedelijkh'] in [str(1), str(2), str(3)]:
        zip_codes.at[i, 'scenario'] = 'UMa'
    elif zip_codes.at[i, 'stedelijkh'] in [str(4), str(5)]:
        zip_codes.at[i, 'scenario'] = 'RMa'
    else:
        print('Unknown stedelijkheid:', zip_codes.at[i, 'stedelijkh'])

    if zip_codes.at[i, 'municipali'] == 'Nuenen, Gerwen en Nederwetten':
        # the code does not like the comma inbetween Nuenen and Gerwen, so I change this municipality.
        zip_codes.at[i, 'municipali'] = 'Nuenen'

# to simplify the geometries for plotting (otherwise the files are too large)
zip_codes['geometry'] = zip_codes['geometry'].simplify(1).buffer(0)

zip_codes.to_file("zip_codes.shp")
