import ijson
from datetime import date
from find_by_id import find_twitter_data_by_ids
import multiprocessing
DATA_PATH = '../../../data/current/'

if __name__ == '__main__':
    objStarted = False

    data = ijson.parse(open(DATA_PATH+'output.json', 'r'))
    scope= ['972Mag', 'Times of Israel', 'Jerusalem Post','Haaretz','Arutz 7','Israel Hayom','Ynet']

    # write the header
    all_referrers ={}
    referrers = []
    id = publisher = ''
    for prefix, event, value in data:
        if prefix.endswith('.id'):
            id = value
            referrers = []
        elif prefix == id+'.referring record id.item':
            referrers.append(value)
        elif prefix.endswith('.associated publisher'):
            publisher = value
            if publisher not in scope:
                id = publisher = ''
                referrers = []
            else:
                if value not in all_referrers:
                    all_referrers[value] = referrers.copy()
                else:
                    all_referrers[value] +=referrers
        if event == "start_map":
            objStarted = True
        if event == "end_map" and objStarted:
            objStarted = False

    # print(all_referrers)
    # print(len(all_referrers["Jerusalem Post"]))
    processes = []
    for publisher in all_referrers:
        process = multiprocessing.Process( target = find_twitter_data_by_ids, args = (all_referrers[publisher],publisher,))
        processes.append(process)
        process.start()
    for proc in processes:
        proc.join()
    
    

        

