import util
import objects.BaseStation
import matplotlib.pyplot as plt

provinces = ['Drenthe', 'Flevoland', 'Friesland', 'Groningen', 'Limburg', 'Overijssel', 'Utrecht', 'Zeeland',
             'Zuid-Holland', 'Gelderland', 'Noord-Brabant', 'Noord-Holland']
# provinces = ['Flevoland']

total_BS = 0
locations = set()

for province in provinces:
    bsfilename = f'{province}all_MNOs'
    all_basestations = util.from_data(f'data/BSs/{bsfilename}_all_basestations.p')
    total_BS += len(all_basestations)

    for BS in all_basestations:
        locations.add((BS.x, BS.y))
    print(len(locations), total_BS)
print(f'In total, there are {total_BS} BS, and {len(locations)} locations. So {1 - len(locations)/total_BS} of the BSs are collocated.')

xs, ys = [], []
for x, y in locations:
    xs.append(x)
    ys.append(y)

plt.scatter(xs,ys)
plt.show()