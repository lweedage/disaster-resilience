from owslib.wfs import WebFeatureService
import xml.etree.ElementTree as ET
import csv

antennes = []

wfs = WebFeatureService('https://geo.zaanstad.nl/geoserver/wfs?SERVICE=WFS&singleTile=true', version='1.1.0')
i = 0

while 1:
    print(f"Fetching from #{i+1}")
    res = wfs.getfeature(typename='geo:antenneregister', sortby=['gemeente'], startindex=i)
    data = res.read()
    text = data.decode('utf-8')
    tree = ET.fromstring(text)
    count = int(tree.attrib['numberOfFeatures'])
    if count == 0: break
    i += count

    for feature in tree:
        assert feature.tag == "{http://www.opengis.net/gml}featureMember", feature.tag
        assert feature[0].tag == "{https://geo.zaanstad.nl/geo}antenneregister", feature[0].tag

        assert feature[0][0].tag == "{https://geo.zaanstad.nl/geo}gemeente"
        assert feature[0][1].tag == "{https://geo.zaanstad.nl/geo}toepassing"
        assert feature[0][2].tag == "{https://geo.zaanstad.nl/geo}ant_hoogte"
        assert feature[0][3].tag == "{https://geo.zaanstad.nl/geo}geom"
        assert feature[0][3][0].tag == "{http://www.opengis.net/gml}Point"
        assert feature[0][3][0].attrib['srsDimension'] == "2"
        assert feature[0][3][0][0].tag == "{http://www.opengis.net/gml}pos"
        easting, northing = feature[0][3][0][0].text.split(" ")

        antennes.append((
            feature[0][0].text, # municpality
            feature[0][1].text, # application
            feature[0][2].text, # height
            # feature[0][3].text, # don't know?
            easting, northing, # EPSG 28992 coordinate
        ))

print("All done!")

with open("antennas.csv", "w", newline='') as f:
    writer = csv.writer(f)
    for antenne in antennes:
        writer.writerow(antenne)