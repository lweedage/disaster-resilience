import pandas as pd
import geopandas as gpd
import cbsodata
import matplotlib.pyplot as plt
from owslib.wfs import WebFeatureService


# Haal de kaart met gemeentegrenzen op van PDOK
wfs = WebFeatureService('https://geodata.nationaalgeoregister.nl/cbspostcode4/wfs?service=WFS', version='1.1.0')
# zip_codes = gpd.read_file(wfs.getfeature(typename='postcode4:postcode42018', sortby=['postcode'], startindex = 0))
#
# print(zip_codes['aantal_inwoners'], zip_codes['postcode'])

i = 0
new_zip_codes = pd.DataFrame()
while 1:
    print(f"Fetching from #{i+1}")
    zip_codes = gpd.read_file(wfs.getfeature(typename='postcode4:postcode42018', sortby=['postcode'], startindex = i))
    count = int(len(zip_codes))
    frames = [zip_codes, new_zip_codes]
    new_zip_codes = pd.concat(frames)
    if count == 0: break
    i += count

print("All done!")

# some population data is negative
for i, x in enumerate(new_zip_codes['aantal_inwoners']):
    if int(x) <= 0:
        new_zip_codes.at[i, 'aantal_inwoners'] = str(0)
    # else:
    #     new_zip_codes.at[i, 'aantal_inwoners'] = int(x)


new_zip_codes.to_pickle('zip_codes.pkl')


