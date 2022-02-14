import json
import requests

url = "https://gisextern.dictu.nl/arcgis/rest/services/Antenneregister/Antennes_extern/MapServer/20/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry={%22xmin%22:0.0,%22ymin%22:289000,%22xmax%22:300000.0,%22ymax%22:629000,%22spatialReference%22:{%22wkid%22:28992}}&geometryType=esriGeometryEnvelope&inSR=28992&outFields=*&outSR=28992"


def find_frequency(freq):
    if freq != '- Hz' and freq != 'Niet aanwezig':
        freq = freq.split(' ')
        if '-' in freq[0]:
            freq[0] = freq[0].split('-')[0]  # if there is a range of frequencies, we take the lowest value

        if freq[1] == 'GHz':
            frequency = float(freq[0]) * 10 ** 9
        elif freq[1] == 'MHz':
            frequency = float(freq[0]) * 10 ** 6
        elif freq[1] == 'kHz':
            frequency = float(freq[0]) * 10 ** 3

        else:
            print('not known frequency: ', freq)

        return frequency


def find_height(h):
    if h != 'Niet aanwezig':
        h = h.split(' ')
        if h[0]:
            return float(h[0])


def find_angle(angle):
    if angle == '0-359,9 gr':
        return 'Omnidirectional'
    else:
        angle = angle.split(' ')
        return float(angle[0])


def find_power(power):
    if power != 'Niet aanwezig':
        power = power.split(' ')
        if power[0]:
            return float(power[0])


def fetch_slice(xmin, mapserver):
    results = dict()
    xmin, xmax = xmin, 5100 + xmin
    ymin, ymax = 289000, 629000
    r = requests.get(
        url=f"https://gisextern.dictu.nl/arcgis/rest/services/Antenneregister/Antennes_extern/MapServer/{mapserver}/query",
        params={
            'f': 'json',
            'returnGeometry': 'true',
            'spatialRel': 'esriSpatialRelIntersects',
            'geometry': json.dumps(
                {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax, 'spatialReference': {'wkid': 28992}}),
            'geometryType': 'esriGeometryEnvelope',
            'inSR': 28992,
            'outFields': 'HOOFDSOORT,X,Y,ID',
            'outSR': 28992
        }).json()

    for feature in r['features']:
        entry = dict()
        entry['ID'] = feature['attributes']['ID']
        entry['type'] = feature['attributes']['HOOFDSOORT']
        entry['x'] = float(feature['geometry']['x'])
        entry['y'] = float(feature['geometry']['y'])
        results[feature['attributes']['ID']] = entry

    pff_IDs = [str(feature['attributes']['ID']) for feature in r['features']]
    print(len(pff_IDs))
    if len(pff_IDs) < 100:
        pff_IDs = ','.join(i for i in pff_IDs)
        IDs = [pff_IDs]
    else:
        slices = []
        i = 0
        while pff_IDs:
            slices.append(pff_IDs[:100])
            pff_IDs = pff_IDs[len(slices[i]):]
            i += 1
        IDs = []
        for row in slices:
            IDs.append([','.join(i for i in row)])

    if IDs:
        r_antennas = dict()
        for row in IDs:
            r_antenna = requests.get(
                url="https://antenneregister.nl/Geocortex/Essentials/REST/sites/Antennes_extern/map/mapservices/9/layers/10/datalinks/DETAILS2_WIMAX/link",
                params={
                    'maxRecords': '', 'pff_ID': row, 'f': 'json'}
            ).json()
            r_antennas.update(r_antenna)

            for antennas in r_antennas['results']:
                ID = int(antennas['featureFieldParameters']['values'][0])
                # find antennas
                ants = dict()
                i = 0
                for antenna in antennas['linkedData']['rows']:
                    ant = dict()
                    ant['height'] = find_height(antenna['row'][1])
                    ant['angle'] = find_angle(antenna['row'][2])
                    ant['frequency'] = find_frequency(antenna['row'][3])
                    ant['power'] = find_power(antenna['row'][4])
                    ants[i] = ant
                    i += 1

                results[ID]['antennas'] = ants
        return results


total_results = dict()

for xmin in range(0, 305000, 5000):
    print('Fetching from x =', xmin / 1000, 'till', (xmin + 5100) / 1000, 'km')

    for mapserver in [7]: #1, 2, 4, 5, 7, 8, 10, 11]:  # different layers of the map: (1,2)GSM/(4,5)UMTS/(7,8)LTE/(10,11)NR
        results = fetch_slice(xmin, mapserver)
        if results:
            total_results.update(results)

with open('antennasLTE.json', 'w') as f:
    json.dump(total_results, f)

# fetch_slice(175100, 1)
