import pandas as pd
import geopandas as gpd
from owslib.wfs import WebFeatureService

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

zip_codes.to_file("zip_codes.shp")

# fig, ax = plt.subplots()
# p = zip_codes.plot(column='popdensity', cmap='hot')
# plt.colorbar(p)
# plt.show()
