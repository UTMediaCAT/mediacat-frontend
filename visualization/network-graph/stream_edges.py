import ijson
import csv

data = ijson.parse(open('interest_output.json', 'r'))

header = ['source', 'referring record id']
limit = 200000
count = 0
arrStarted = False
id = ''
with open('interest_output_edges.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    for prefix, event, value in data:
        if prefix.endswith('.id'):
            count = count + 1
            if count > limit:
                break
            id = value
            arrStarted = False
        elif prefix.endswith('.hit count'):
            if value == 0:
                break
        elif prefix.endswith('.referring record id') and event == 'start_array':
            arrStarted = True
        elif arrStarted and event == 'end_array':
            arrStarted = False
        elif event == 'string' and arrStarted:
            writer.writerow([id, value])
# only output to csv for now
# will add visualization later
f.close()
