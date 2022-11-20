import json

# with open('antennasGSM.json') as f1:
#     GSM = json.load(f1)
with open('antennasLTE.json') as f2:
    LTE = json.load(f2)
with open('antennasNR.json') as f3:
    NR = json.load(f3)
with open('antennasUMTS.json') as f4:
    UMTS = json.load(f4)

antennas=dict()
# antennas.update(GSM)
antennas.update(LTE)
antennas.update(NR)
antennas.update(UMTS)

with open('antennas.json', 'w') as f:
    json.dump(antennas, f)

