import ijson
import csv
import json
header = ['source', 'hit count']


data = ijson.parse(open('interest_output.json', 'r'))

limit = 200000
count = 0
jsonObj = {}

# write the header
id = source = hit_count = ''
for prefix, event, value in data:
    if count > limit:
        break
    if prefix.endswith('.id'):
        count = count + 1
        if count > limit:
            break
        id = source = url = hit_count = ''
        id = value
    elif prefix.endswith('.hit count'):
        if value == 0:
            break
        hit_count = value
    elif prefix.endswith('.source'):
        source = value
        if source in jsonObj:
            jsonObj[source] += int(hit_count)
        else:
            jsonObj[source] = int(hit_count)

# only output to csv for now
# will add visualization later
with open('source_count.json', 'w') as outfile:
    json.dump(jsonObj, outfile)
