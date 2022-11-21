import geopandas as gpd


def find_scenario(stedelijkheid):
    if stedelijkheid in [1, 2, 3]:
        return 'UMA'
    else:
        return 'RMA'


# the 500*500 m square statistics from Statistics Netherlands: https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data/kaart-van-500-meter-bij-500-meter-met-statistieken
zip_codes = gpd.read_file('cbs_vk500_2020_v2.gpkg')

zip_codes['aantal_inwoners'] = zip_codes['aantal_inwoners'].astype(int)
zip_codes = zip_codes.filter(['postcode', 'aantal_inwoners', 'stedelijkheid', 'geometry'],
                             axis=1)  # filter data set with only what we need
zip_codes = zip_codes[~zip_codes['geometry'].isnull()]  # Remove rows with empty geometry
zip_codes = zip_codes[~zip_codes['aantal_inwoners'] <= 0]  # Remove rows with no population

municipalities = gpd.read_file(
    "gemeente_2020_v3.shp")  # data from https://www.cbs.nl/nl-nl/dossier/nederland-regionaal/geografische-data/wijk-en-buurtkaart-2020
municipalities = municipalities.loc[municipalities['H2O'] == 'NEE']  # Remove all water areas in municipalities

for index, row in zip_codes.iterrows():
    print(index)
    geom = row['geometry']
    for index_m, row_m in municipalities.iterrows():
        if row_m['geometry'].intersects(geom):
            zip_codes.loc[index, 'municipality'] = municipalities.loc[index_m, 'GM_NAAM']
            continue

zip_codes['scenario'] = [find_scenario(int(stedelijkheid)) for stedelijkheid in zip_codes['stedelijkheid']]

zip_codes.to_file("square_statistics.shp")
