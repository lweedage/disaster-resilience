import pandas as pd
import geopandas as gpd

# the 500*500 m square statistics from Statistics Netherlands: https://www.cbs.nl/nl-nl/longread/diversen/2022/statistische-gegevens-per-vierkant-2021-2020-2019
zip_codes = gpd.read_file('cbs_vk500_2020_v2.gpkg')

zip_codes['aantal_inwoners'] = zip_codes['aantal_inwoners'].astype(int)
zip_codes = zip_codes.filter(['postcode', 'aantal_inwoners', 'stedelijkheid', 'geometry'],axis=1)  # filter data set with only what we need
zip_codes = zip_codes[~zip_codes['geometry'].isnull()]  # Remove rows with empty geometry
zip_codes = zip_codes[~zip_codes['aantal_inwoners'] <= 0]  # Remove rows with no population

municipalities = gpd.read_file("gemeente_2020_v2.shp")
municipalities = municipalities.loc[municipalities['H2O'] == 'NEE'] # Remove all water areas in municipalities

for index, row in zip_codes.iterrows():
    geom = row['geometry']
    for index_m, row_m in municipalities.iterrows():
        if row_m['geometry'].intersects(geom):
            zip_codes.loc[index, 'municipality'] = municipalities.loc[index_m, 'GM_NAAM']
            continue

zip_codes.to_file("square_statistics.shp")
