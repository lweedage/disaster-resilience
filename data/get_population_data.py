import pandas as pd
import geopandas as gpd
from owslib.wfs import WebFeatureService
from shapely.geometry import Polygon, MultiPolygon
import csv

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# TODO add population data based on age groups?
# TODO or maybe vierkantstatitistieken (per 100 m?) - CBS Vierkantstatistieken 100m WFS
# Get zip code data from PDOK
wfs = WebFeatureService('https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?service=WfS', version='1.1.0')

i = 0
zip_codes = pd.DataFrame()
while 1:
    print(f"Fetching from #{i + 1}")
    add_zip_codes = gpd.read_file(wfs.getfeature(typename='postcode4:postcode42020', sortby=['postcode'], startindex=i))
    count = int(len(add_zip_codes))
    frames = [add_zip_codes, zip_codes]
    zip_codes = pd.concat(frames)
    if count == 0: break
    i += count

print("All done!")

# Find the corresponding municipality of the zip codes ------------------------------------------------
with open("zipcode_to_municipality_number.csv", "r") as f:
    reader = csv.reader(f, delimiter = ';')
    next(reader, None)
    lines = list(reader)

municipality_code = dict()
for line in lines:
    municipality_code[line[0][:-2]] = int(line[3])
municipality_code['9914'] = 24
municipality_code['9915'] = 24

with open("municipalities.csv", "r") as f:
    reader = csv.reader(f, delimiter = ';')
    next(reader, None)
    lines = list(reader)

code = dict()
for line in lines:
    code[int(line[0])] = line[1]

zip_code_to_municipality = {key: code[value] for key, value in municipality_code.items()}
# ---------------------------------------------------------------------------------------

zip_codes['aantal_inwoners'] = zip_codes['aantal_inwoners'].astype(int)
zip_codes['postcode'] = zip_codes['postcode'].astype(int)
zip_codes = zip_codes.filter(['postcode', 'aantal_inwoners', 'stedelijkheid', 'geometry'],
                             axis=1)  # filter data set with only what we need
zip_codes = zip_codes[~zip_codes['geometry'].isnull()]  # Remove rows with empty geometry
zip_codes = zip_codes[~zip_codes['aantal_inwoners'] <= 0]  # Remove rows with no population

# -----------------------------------------------------------------------------------
# bit of an ugly fix, but there is a mistake in the geometry of zip code 8251
poly = zip_codes[(zip_codes['postcode'] == 8251)]['geometry']
problem = list(list(poly)[0])[4]
exteriors, interiors = problem.exterior, problem.interiors
changed_polygon = Polygon(exteriors, [[pt for pt in inner.coords] for inner in interiors[3:]])
total_polygon = MultiPolygon(
    [list(list(poly)[0])[0], list(list(poly)[0])[1], list(list(poly)[0])[2], list(list(poly)[0])[3], changed_polygon])

row_to_remove = zip_codes[(zip_codes['postcode'] == 8251)]
zip_codes.drop(row_to_remove.index[0], inplace=True)

data = {'postcode': 8251, 'geometry': gpd.GeoSeries(total_polygon),
        'aantal_inwoners': row_to_remove['aantal_inwoners'].values, 'stedelijkheid': row_to_remove['stedelijkheid'].values}
new_df = gpd.GeoDataFrame(data)
zip_codes = gpd.GeoDataFrame(pd.concat([zip_codes, new_df], ignore_index=True))
# -----------------------------------------------------------------------------------

zip_codes['popdensity'] = zip_codes['aantal_inwoners'] / zip_codes[
    'geometry'].area  # add population density: number of people divided by area
zip_codes['municipality'] = [zip_code_to_municipality[str(p)] for p in zip_codes['postcode']]
zip_codes.to_file("zip_codes.shp")
