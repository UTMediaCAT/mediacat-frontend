import ijson
import csv
import json
header = ['id', 'url or alias text', 'url',
          'referrer id', 'referrer url', 'date of publication']


limit = 5000000
count = 0
objStarted = False
id_to_obj = {}
DATA_PATH = '../../data/current/'

data1 = ijson.parse(open(DATA_PATH+'interest_output.json', 'r'))
id = url = hit_count = ''
for prefix, event, value in data1:
    if count > limit:
        break
    if prefix.endswith('.id'):
        count = count + 1
        if count > limit:
            break
        id = value
    elif prefix.endswith('.hit count'):
        hit_count = value
    elif prefix.endswith('.url or alias text'):
        id_to_obj[id] = {"url": value}
    elif prefix.endswith('.date of publication'):
        id_to_obj[id]["date"] = value
print(len(id_to_obj))
print(id)

count = 0
objStarted = False

data = ijson.parse(open(DATA_PATH+'output.json', 'r'))

# keep track of found ids so we only write them once
found = []

# write the header
with open("input_for_stacked_area_graph.csv", 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    referrers = {}
    id = url = hit_count = ''
    for prefix, event, value in data:
        if count > limit:
            break
        if prefix.endswith('.id'):
            count = count + 1
            if count > limit:
                break
            id = value
        elif prefix.endswith('.number of referrals'):
            if value == 0:
                break
            hit_count = value
        elif prefix.endswith('.url or alias text'):
            url = value
        elif prefix == id+'.referring record id.item':
            # print(value in id_to_url)
            if value not in referrers and value not in found:
                referrers[value] = id_to_obj[str(value)]
                found.append(value)
        if event == "start_map":
            objStarted = True
        if event == "end_map" and objStarted:
            for r in referrers:
                writer.writerow(
                    [r, referrers[r]["url"], "null", "null", "null", "null", "null", "null", "null", "null", referrers[r]["date"], "null", "null", "null"])
            id = url = hit_count = ''
            referrers = {}
            objStarted = False
f.close()
