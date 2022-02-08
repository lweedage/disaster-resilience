import pandas as pd
import geopandas as gpd
from owslib.wfs import WebFeatureService
from shapely.geometry import Polygon, MultiPolygon

# Get zip code data from PDOK
wfs = WebFeatureService('https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?service=WFS', version='1.1.0')

i = 0
zip_codes = pd.DataFrame()
while 1:
    print(f"Fetching from #{i + 1}")
    add_zip_codes = gpd.read_file(wfs.getfeature(typename='postcode4:postcode42018', sortby=['postcode'], startindex=i))
    count = int(len(add_zip_codes))
    frames = [add_zip_codes, zip_codes]
    zip_codes = pd.concat(frames)
    if count == 0: break
    i += count

print("All done!")

zip_codes['aantal_inwoners'] = zip_codes['aantal_inwoners'].astype(int)
zip_codes['postcode'] = zip_codes['postcode'].astype(int)
zip_codes['popdensity'] = zip_codes['aantal_inwoners'] / zip_codes['geometry'].area
zip_codes = zip_codes.filter(['postcode', 'aantal_inwoners', 'popdensity', 'geometry'],
                             axis=1)  # filter data set with only what we need
zip_codes = zip_codes[~zip_codes['geometry'].isnull()] # Remove rows with empty geometry

#-----------------------------------------------------------------------------------
# bit of an ugly fix, but there is a mistake in the geometry of zip code 8251
poly = zip_codes[(zip_codes['postcode'] == 8251)]['geometry']
problem = list(list(poly)[0])[4]
exteriors, interiors = problem.exterior, problem.interiors
changed_polygon = Polygon(exteriors, [[pt for pt in inner.coords] for inner in interiors[3:]])
total_polygon = MultiPolygon([list(list(poly)[0])[0], list(list(poly)[0])[1], list(list(poly)[0])[2], list(list(poly)[0])[3], changed_polygon])

row_to_remove = zip_codes[(zip_codes['postcode'] == 8251)]
zip_codes.drop(row_to_remove.index[0], inplace = True)

data = {'postcode': 8251, 'geometry': gpd.GeoSeries(total_polygon), 'aantal_inwoners': row_to_remove['aantal_inwoners'].values, 'popdensity': row_to_remove['popdensity'].values}
new_df = gpd.GeoDataFrame(data)
zip_codes = gpd.GeoDataFrame( pd.concat( [zip_codes, new_df], ignore_index=True) )
#-----------------------------------------------------------------------------------

zip_codes.to_file("zip_codes.shp")

# fig, ax = plt.subplots()
# p = zip_codes.plot(column='popdensity', cmap='hot')
# plt.colorbar(p)
# plt.show()
