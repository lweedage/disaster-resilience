import geopandas as gpd
import find_base_stations as antenna
from shapely.geometry import Point
from shapely.ops import unary_union
from util import BaseStationRadioType

zip_codes = gpd.read_file('zip_codes.shp')

# for i, row in zip_codes.iterrows():
#     print(i)
#     GSM, UMTS, LTE, NR = 0, 0, 0, 0
#     region = gpd.GeoSeries(unary_union(row['geometry']))
#     base_stations = antenna.load_bs(region)
#     for BS in base_stations:
#         if BS.radio == BaseStationRadioType.GSM:
#             GSM += 1
#         elif BS.radio == BaseStationRadioType.UMTS:
#             UMTS += 1
#         elif BS.radio == BaseStationRadioType.LTE:
#             LTE += 1
#         elif BS.radio == BaseStationRadioType.NR:
#             NR += 1
#     zip_codes.at[i, 'GSM_BS'] = GSM
#     zip_codes.at[i, 'UMTS_BS'] = UMTS
#     zip_codes.at[i, 'LTE_BS'] = LTE
#     zip_codes.at[i, 'NR_BS'] = NR
#     zip_codes.at[i, 'BSs'] = GSM + UMTS + LTE + NR
#
# zip_codes['BS_to_users'] = zip_codes['BSs'] / zip_codes['aantal_inw']


for i, row in zip_codes.iterrows():
    print(i)
    if zip_codes.at[i, 'stedelijkh'] in [str(1), str(2)]:
        zip_codes.at[i, 'scenario'] = 'UMi'
    elif zip_codes.at[i, 'stedelijkh'] in [str(3), str(4)]:
        zip_codes.at[i, 'scenario'] = 'UMa'
    else:
        zip_codes.at[i, 'scenario'] = 'RMa'

zip_codes.to_file("zip_codes_with_scenarios.shp")
