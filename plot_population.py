import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

zip_codes = pd.read_pickle('zip_codes.pkl')

print(zip_codes['aantal_inwoners'])

# for i, x in enumerate(zip_codes['aantal_inwoners']):
#     print(i, x)
#     if int(x) <= 0:
#         zip_codes.at[i, 'aantal_inwoners'] = str(0)
#         print(i, x)
    # else:
    #     zip_codes.at[i, 'aantal_inwoners'] = int(x)

p = zip_codes.plot(column = 'aantal_inwoners', cmap = 'hot', legend = True)
plt.colorbar(p)
plt.show()