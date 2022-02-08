import requests
import csv
import json
# code from Bart Meyers - it does not work for me yet.

URL_ID_DELIM = "%2C"
base_api_url = "https://antenneregister.nl/Geocortex/Essentials/REST/sites/Antennes_extern/map/mapservices/9/layers/10/datalinks/DETAILS2_WIMAX/link?maxRecords=&f=json&pff_ID="

antennes = []

def read_csv(f):
    '''
    Reads csv and returns list of dicts
    One dict for each line in the csv
    :param f: file
    '''
    result = []
    reader = csv.DictReader(f)
    for row in reader:
        result.append(row)
    return result

# Load antenna csv's
# with open('AB_LTE.csv', newline='') as f:
#     antennes = read_csv(f)

with open('AB_5GNR.csv', newline='') as f:
    antennes += read_csv(f)

# Load additional info on the antennas
for antenne in antennes:
    pff_ID = antenne.get('ID')
    response = requests.get(f"{base_api_url}{pff_ID}")
    print(response.json())
    if len(response.json().get('results')) != 0:
        linkedData = response.json().get('results')[0].get('linkedData')
        antenne_types = []
        columns = linkedData.get('columns')
        for row in linkedData.get('rows'):
            info = row.get('row')
            d = dict()
            d[columns[1]] = info[1]
            d[columns[2]] = info[2]
            d[columns[3]] = info[3]
            d[columns[4]] = info[4]
            antenne_types.append(d)

        antenne['antennes'] = antenne_types

# Save data as json
with open("antennes.json", "w+") as f:
    json.dump(antennes, f, indent=4)

# Save all data to new csv
#with open("antennes.csv", 'w+', newline='') as f:
#    writer = csv.DictWriter(f)
#    for antenne in antennes:
#        writer.writerow(antenne)